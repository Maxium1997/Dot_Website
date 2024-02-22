from enum import Enum


class EquipmentType(Enum):
    other = (5000, 'Other', '其他')

    optical_drive = (1001, 'Optical Drive', '光碟機')
    digital_audio_recorder = (1002, 'Digital Audio Recorder', '數位錄音機')
    external_floppy_disk_drive = (1003, 'External Floppy Disk Drive', '外接式軟碟機')
    external_burner = (1004, 'External Burner', '外接式燒錄機')
    digital_camera = (1005, 'Digital Camera', '數位相機／攝影機')
    wireless_barcode_scanner = (1006, 'Wireless Barcode Scanner', '無線條碼識別器')
    card_reader = (1007, 'Card Reader', '讀卡機')
    driving_recorder = (1008, 'Driving Recorder')

    thumb_drive = (2001, 'Thumb Drive', '隨身碟')
    external_hard_disk_drive = (2002, 'External Hard Disk Drive', '外接式硬碟')
    memory_card = (2003, 'Memory Card', '記憶卡')


class StorageUnit(Enum):
    KB = (1, 'KB')
    MB = (2, 'MB')
    GB = (3, 'GB')
    TB = (4, 'TB')


class CertificateUsage(Enum):
    Personal = (1, 'Personal', '個人憑證申請')
    Agency = (2, 'Agency', '機關（單位）憑證申請')
    Server = (3, 'Server', '伺服器憑證申請')


class CertificateCustodianClassification(Enum):
    Unit = (1, 'Unit', '單位卡')
    VoluntaryMilitary = (2, 'Voluntary Military', '志願役')
    ObligatoryMilitary = (3, 'Obligatory Military', '義務役')
    CivilServant = (4, 'CivilServant', '文職')
    Police = (5, 'Police', '警職')
    Outsource = (6, 'Outsource', '廠商')


class CertificateStorage(Enum):
    ICCard = (1, 'IC Card', '智慧卡')
    MagneticDisk = (2, 'Magnetic Disk', '磁片')


class CertificateProcess(Enum):
    Apply = (1, 'Apply', '申請')
    Undo = (2, 'Undo', '撤銷')
    Reissue = (3, 'Reissue', '補發')
    ReportALoss = (4, 'Report a Loss', '掛失')
    Recover = (5, 'Recover', '復原')
    Reschedule = (6, 'Reschedule', '展期')


class CertificateUseFor(Enum):
    Duty = (1, 'Duty', '勤務使用')
    Business = (2, 'Business', '業務使用')
    SystemUsing = (3, 'System Using', '系統使用需求')
    Register = (4, 'Register', '新進報到')
    NewPosition = (5, 'New Position', '新職報到')
    TransferPosition = (6, 'Transfer Position', '調職')
    Retirement = (7, 'Retirement', '退伍')
    ChangeSoftCer = (8, 'Change Soft Certificate', '更換軟憑')
    BrokenReApply = (9, 'Broken Reapply', '卡片毀損，重新申請')


class OceanStationServiceItems(Enum):
    Lounge = (0b1, 'Lounge', '民眾休息區')
    AccessibleRestroom = (0b10, 'AccessibleRestroom', '無障礙廁所')
    DrinkingFountain = (0b100, 'DrinkingFountain', '飲水機')
    CleaningFacility = (0b1000, 'CleaningFacility', '沖洗設施')
    Lockers = (0b10000, 'Lockers', '置物櫃')
    ParkingLot = (0b100000, 'ParkingLot', '停車場')
    LifeVestRent = (0b1000000, 'LifeVestRent', '救生衣租借')
