class CloudUser:
    customerid = None
    email = ""
    password = ""
    support_admin = False
    phone_number = ""
    enabled = True
    msp = None
    two_factor = False
    demo_account = False
    attributes = ["customerid", "email", "password", "support_admin", "phone_number", "enabled", "two_factor", "msp", "demo_account"]

    def __init__(self, customerid=None, email=None, password=None, enabled=True, phone_number=None, two_factor=False):
        self.customerid = customerid
        self.email = email
        self.password = password
        self.enabled = enabled
        self.phone_number = phone_number
        self.two_factor = two_factor

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.enabled

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.customerid

    def load_attributes_from_dict(self, dict_obj):
        for (key, val) in dict_obj.items():
            setattr(self, key, val)
            if key not in self.attributes:
                self.attributes.append(key)

    def to_dict(self):
        obj_rep = {}
        for attribute in self.attributes:
            if hasattr(self, attribute):
                obj_rep[attribute] = getattr(self, attribute)
        return obj_rep


class CloudDevice:
    deviceid = None
    key = None
    description = None
    user_defined_name = None
    routed_network = True
    timezone = None
    monitored = False
    last_version = None
    edgewize = False
    surfwize = False
    report_emails = None
    labels = []
    white_label_file_name = None
    classroom_groups = None
    mylinewize_login = None
    beta_tester = False
    paid_subscription = False
    reseller = None
    hardware = None
    customer_type = None
    education_institute_number = 0
    deal_url = None
    active = True
    invoice_number = 0
    install_date = None
    classroom_exceptions = None
    classroom_allow_owner_access = False
    classroom_restrict_global_teachers = False
    allow_public_source_ip = False
    failover_active = False
    stats_active = True
    inventory = None
    update_allow_auto = None
    update_branch = None
    classroom_groups_group_prefix = None
    watchdog_recipients = []
    xero_id = None
    msp = None
    classwize_reliever_enabled = False
    logging_configuration__upload_ttl = 0
    logging_configuration__flush_files = 0
    teacher_classrooms_enabled = False
    mobilezone_enabled = False
    mobilezone_groups = []

    # If you add an attribute to this class, MAKE SURE YOU ADD IT TO THIS LIST
    attributes = ["deviceid", "description", "user_defined_name",
                  "routed_network", "timezone",
                  "key", "monitored",
                  "last_version", "edgewize", "surfwize", "report_emails", "labels",
                  "white_label_file_name", "classroom_groups", "classroom_exceptions", "mylinewize_login", "beta_tester",
                  "paid_subscription", "reseller", "hardware",
                  "customer_type", "education_institute_number", "deal_url", "active", "invoice_number", "install_date",
                  "allow_public_source_ip", "failover_active", "stats_active", "classroom_allow_owner_access",
                  "classroom_restrict_global_teachers", "inventory", "update_allow_auto",
                  "update_branch", "classroom_groups_group_prefix",
                  "watchdog_recipients", "xero_id", "msp", "classwize_reliever_enabled",
                  "logging_configuration__upload_ttl", "logging_configuration__flush_files", 
                  "teacher_classrooms_enabled", "mobilezone_enabled", "mobilezone_groups"]

    def __init__(self, deviceid=None, description=""):
        self.deviceid = deviceid
        self.description = description

    def load_attributes_from_dict(self, dict_obj):
        for (key, val) in dict_obj.items():
            setattr(self, key, val)
            if key not in self.attributes:
                self.attributes.append(key)

    def to_dict(self):
        obj_rep = {}
        for attribute in self.attributes:
            if hasattr(self, attribute):
                obj_rep[attribute] = getattr(self, attribute)
        return obj_rep


class CloudMyLinewizeUserGroupMapping:

    id = None
    deviceid = None
    user = ""
    groups = []
    attributes = ["deviceid", "user", "groups"]

    def __init__(self, id=None, deviceid=None, user="", groups=[]):
        self.id = id
        self.deviceid = deviceid
        self.user = user
        self.groups = groups

    def load_attributes_from_dict(self, dict_obj):
        if dict_obj:
            for (key, val) in dict_obj.items():
                setattr(self, key, val)
                if key not in self.attributes:
                    self.attributes.append(key)

    def to_dict(self):
        obj_rep = {}
        for attribute in self.attributes:
            if hasattr(self, attribute):
                obj_rep[attribute] = getattr(self, attribute)
        return obj_rep


class CloudDeviceStats:

    deviceid = None
    last_status = False
    last_version = None
    last_os_version = None
    last_online_timestamp = 0
    last_uptime = 0
    last_maintenance = False
    last_status_offline_time = 0
    last_status_offline_notified = False
    attributes = ["deviceid", "last_status", "last_version", "last_os_version",
                  "last_online_timestamp", "last_uptime", "last_maintenance",
                  "last_status_offline_time", "last_status_offline_notified"]

    def __init__(self, deviceid=None):
        self.deviceid = deviceid

    def load_attributes_from_dict(self, dict_obj):
        if dict_obj:
            for (key, val) in dict_obj.items():
                setattr(self, key, val)
                if key not in self.attributes:
                    self.attributes.append(key)

    def to_dict(self):
        obj_rep = {}
        for attribute in self.attributes:
            if hasattr(self, attribute):
                obj_rep[attribute] = getattr(self, attribute)
        return obj_rep
