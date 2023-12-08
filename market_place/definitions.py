from enum import Enum


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
