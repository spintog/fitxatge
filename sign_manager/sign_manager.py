import requests
from lxml import html

class SignManager():
    """
    A class used manage user's time work.

    ...

    Attributes
    ----------
    token : str
        string that identifies user
    url : str
        string with base URL server

    Methods
    -------
    get_zid
        create a GET query
    get_status
        get current user's status
    """
    
    def __init__(self, config):
        
        """
        Constructor with config parametres received in a dictionary

        ...
        Config parameters
        -----------------
        config["token"]
            user's token
        config["base_url"]
            Server URL
        """
        self.token = config["token"]
        self.base_url = config["base_url"]
        self.session = requests.Session()

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, user_token):
        if user_token:
            self._token = user_token
        else:
            raise ValueError("User's token not found. Verify config parameters")

    @property
    def base_url(self):
        return self.base_url
    
    @base_url.setter
    def base_url(self, base_url):
        if base_url:
            self._base_url = base_url
        else:
            raise ValueError("URL not found. Verify config parameters")

    def get_zid(self):
        """
        Method to find user's zid. Necessari to make queries.
        """

        r = self.session.get(self._base_url+"/marcaje.php?access-token={}".format(self._token))
        tree = html.fromstring(r.content)
        data = tree.xpath("//a[@data-zid]")

        for element in data:
            zid = element.get("data-zid")
        
        if zid:
            return zid
        else:
            return False

    def get_status(self):
        """
        Method to get the current user's status
        """
        zid = self.get_zid()
        if zid:
            parameters = {
                "zid": zid
            }
        else:
            return ValueError("ZID not found")

        r = self.session.post(self._base_url+"/estado-actual.php", data = parameters)
        if "AUSENTE" in r.text:
            return False
        else:
            return True

    def change_status(self):
        """
        Method to change sign status
        """
        current_status = self.get_status()

        zid = self.get_zid()
        if zid: 
            parameters = {
                "access-token": self._token,
                "zid": zid,
            }
            self.session.close()
        else:
            return "ZID not found"

        r = self.session.post(self._base_url+"/fichaje.php", data = parameters)
        if self.get_status() != current_status:
            return True
        else:
            return r.status_code

    def get_server_status(self):
        """
        Method to check server status.
        """

        try:
            self.session.get(self._base_url+"/marcaje.php?access-token={}".format(self._token), timeout=5)
            return True
        except requests.exceptions.Timeout:
            return False
