import requests,os

class download:    
    
    def exec(self, url, adminAccount, localFilename):
        self.createPathIfNotExixts(localFilename)
        requests.packages.urllib3.disable_warnings()
        with requests.get(url, stream=True, verify=False, auth=tuple(adminAccount)) as r:
            r.raise_for_status()
            with open(localFilename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
    
    def createPathIfNotExixts(self, rawPath):
        path = os.path.dirname(rawPath.replace("\\","/"))        
        if (path and not os.path.exists(path)):
            print('Creo la directory %s ' % (path))
            os.makedirs(path)