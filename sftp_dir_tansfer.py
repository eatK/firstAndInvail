import os
import paramiko
import pysftp
from stat import S_ISDIR as isdir

class sftp:
#建立连接，获取sftp句柄
    def sftp_connect_key(username,host,key_file,port=22):
        client = None
        sftp = None
        try:
            private_key = paramiko.RSAKey.from_private_key_file(key_file)
            client = paramiko.Transport((host,port))
        except Exception as error:
            print (1,error)

        try:
            client.connect(username=username,pkey=private_key)
        except Exception as error:
            print (2,error)
        else:
            sftp = paramiko.SFTPClient.from_transport(client)
        return client,sftp

    #建立连接，获取sftp句柄
    def sftp_connect_u_p(username,host,password,port=22):
        client = None
        sftp = None
        try:
            client = paramiko.Transport((host,port))
        except Exception as error:
            print (1,error)
        else:
            try:
                client.connect(username=username, password=password)
            except Exception as error:
                print (2,error)
            else:
                sftp = paramiko.SFTPClient.from_transport(client)
        return client,sftp

    #断开连接
    def disconnect(client):
        try:
            client.close()
        except Exception as error:
            print (error)

    def _check_local(local):
        if not os.path.exists(local):
            try:
                os.mkdir(local)
            except IOError as err:
                print(err)

    def get(self,sftp,remote,local):
        #检查远程文件是否存在
        try:
            result = sftp.stat(remote)
        except IOError as err:
            error = '[ERROR %s] %s: %s' %(err.errno,os.path.basename(os.path.normpath(remote)),err.strerror)
            print (error)

        #判断远程文件是否为目录
        if isdir(result.st_mode):
            dirname = os.path.basename(os.path.normpath(remote))
            local = os.path.join(local,dirname)
            self._check_local(local)
            for file in sftp.listdir(remote):
                sub_remote = os.path.join(remote,file)
                sub_remote = sub_remote.replace('\\','/')
                self.get(sftp,sub_remote,local)
        else:
        #拷贝文件
            if os.path.isdir(local):
                local = os.path.join(local,os.path.basename(remote))
            try:
                sftp.get(remote,local)
                print(1)
            except IOError as err:
                print(err)
            else:
                print ('[get]',local,'<==',remote)

    def __init__(self):
        pass

# client,sftp=sftp_connect_key('administrator','10.206.33.147','/root/workplace/mysite_my/ssh_host_rsa_key',8000)
# print(1,client,2,sftp)
# get(sftp,remote,local)
# put(sftp,remote,local)
# disconnect(client)
