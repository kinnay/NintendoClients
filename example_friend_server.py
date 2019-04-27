from nintendo.nex import service, backend, authentication, common, kerberos, secure, friends
from nintendo.games import Friends

import logging

logger = logging.getLogger(__name__)


class Success(common.Result):
    def __init__(self):
        super(Success, self).__init__(0x10001)


# kerberos.key_size
SECURE_SERVER_KEY = b'P' * 16


def get_kerberos_key_for_user(key_derivation, pid):
    # TODO actually implement this by looking up the NEX password for the pid in the database
    if pid == 1337:
        return key_derivation.derive_key(
            "password".encode("ascii"), pid
        )
    else:
        raise common.RMCError("RendezVous::InvalidUsername")


class MyAuthenticationServer(authentication.AuthenticationServer):
    def __init__(self, settings):
        super(MyAuthenticationServer, self).__init__()
        self.settings = settings
        if self.settings.get("kerberos.key_derivation") == 0:
            self.key_derivation = kerberos.KeyDerivationOld(65000, 1024)
        else:
            self.key_derivation = kerberos.KeyDerivationNew(1, 1)

    def login(self, caller_id, response, username):
        print("AuthenticationServer.login(caller_id: %s, username: %s)" % (caller_id, username))

        pid = int(username)

        # Derive kerberos key from password
        kerberos_key = get_kerberos_key_for_user(self.key_derivation, pid)

        session_key = b'L' * self.settings.get("kerberos.key_size")

        ticket = kerberos.ClientTicket(b'')
        ticket.target_pid = 1
        ticket.session_key = session_key
        ticket.internal = 68 * b'I'

        main_station = common.StationUrl.parse("prudps:/address=127.0.0.1;port=60021;CID=1;PID=2;sid=1;stream=10;type=2")

        connection_data = authentication.RVConnectionData()
        connection_data.main_station = main_station
        connection_data.special_protocols = []
        connection_data.special_station = ""

        response.result = Success()
        response.pid = pid
        response.ticket = ticket.encrypt(kerberos_key, self.settings)
        response.connection_data = connection_data
        response.server_name = "branch:origin/project/nfs build:3_10_18_2006_0"

    def login_ex(self, *args):
        logger.warning("AuthenticationServer.login_ex not implemented")
        raise common.RMCError("Core::NotImplemented")

    def request_ticket(self, caller_id, response, source, target):
        print("AuthenticationServer.request_ticket(caller_id: %s, source: %u, target: %u)" % (caller_id, source, target))
        # Derive kerberos key from password
        kerberos_key = get_kerberos_key_for_user(self.key_derivation, source)

        session_key = b'R' * self.settings.get("kerberos.key_size")

        internal = kerberos.ServerTicket(b'')
        internal.expiration = common.DateTime.make(27, 4, 2020, 12, 0, 0)
        internal.source_pid = source
        internal.session_key = session_key

        ticket_key = b'&' * 16
        internal_encrypted = internal.encrypt(SECURE_SERVER_KEY, ticket_key, self.settings)

        ticket = kerberos.ClientTicket(b'')
        ticket.target_pid = target
        ticket.session_key = session_key
        ticket.internal = internal_encrypted

        response.result = Success()
        response.ticket = ticket.encrypt(kerberos_key, self.settings)

    def get_pid(self, username):
        logger.warning("AuthenticationServer.get_pid not implemented")
        raise common.RMCError("Core::NotImplemented")

    def get_name(self, pid):
        logger.warning("AuthenticationServer.get_name not implemented")
        raise common.RMCError("Core::NotImplemented")


class MySecureConnectionServer(secure.SecureConnectionServer):
    def __init__(self, settings):
        super(MySecureConnectionServer, self).__init__()
        self.settings = settings

    def register(self, caller_id, response, urls):
        logger.warning("SecureConnectionServer.register not implemented")
        raise common.RMCError("Core::NotImplemented")

    def request_connection_data(self, caller_id, response, cid, pid):
        logger.warning("SecureConnectionServer.request_connection_data not implemented")
        raise common.RMCError("Core::NotImplemented")

    def request_urls(self, caller_id, response, cid, pid):
        logger.warning("SecureConnectionServer.request_urls not implemented")
        raise common.RMCError("Core::NotImplemented")

    def register_ex(self, caller_id, response, urls, login_data):
        print("SecureConnectionServer.register_ex(caller_id: %d, urls: %s, login_data: %s)" % (caller_id, urls, login_data.token))
        response.result = Success()
        response.connection_id = 42
        response.public_station = urls[0]

    def test_connectivity(self):
        logger.warning("SecureConnectionServer.test_connectivity not implemented")
        raise common.RMCError("Core::NotImplemented")

    def replace_url(self, url, new):
        logger.warning("SecureConnectionServer.replace_url not implemented")
        raise common.RMCError("Core::NotImplemented")

    def send_report(self, report_id, data):
        logger.warning("SecureConnectionServer.send_report not implemented")
        raise common.RMCError("Core::NotImplemented")


class MyFriendsServer(friends.FriendsServer):
    def __init__(self, settings):
        super(MyFriendsServer, self).__init__()
        self.settings = settings

    def get_all_information(self, caller_id, response, nna_info, presence, birthday):
        print("MyFriendsServer.get_all_information(caller_id: %d, nna_info: %s, presence: %s, birthday: %s" % (caller_id, nna_info, presence, birthday))
        principal_preference = friends.PrincipalPreference()
        principal_preference.unk1 = True
        principal_preference.unk2 = True
        principal_preference.unk3 = False

        comment = friends.Comment()
        comment.unk = 0
        comment.text = ""
        comment.changed = common.DateTime(0)

        response.principal_preference = principal_preference
        response.comment = comment
        response.friends = []
        response.sent_requests = []
        response.received_requests = []
        response.blacklist = []
        response.unk1 = False
        response.notifications = []
        response.unk2 = False

    def update_presence(self, presence):
        logger.warning("FriendsServer.update_presence not implemented")
        raise common.RMCError("Core::NotImplemented")


def main():
    friends_settings = backend.Settings("friends.cfg")
    friends_settings.set("server.access_key", Friends.ACCESS_KEY)

    s1 = service.RMCServer(friends_settings)
    authentication_protocol = MyAuthenticationServer(friends_settings)

    s1.register_protocol(authentication_protocol)
    s1.start("127.0.0.1", 60000, 1)

    s2 = service.RMCServer(friends_settings)
    s2.register_protocol(MySecureConnectionServer(friends_settings))
    s2.register_protocol(MyFriendsServer(friends_settings))
    s2.start("127.0.0.1", 60021, 1, SECURE_SERVER_KEY)

    while True:
        pass


if __name__ == "__main__":
    main()
