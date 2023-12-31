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
    SystemUsing = (3, 'System Using', '系統使用需求')
    Register = (4, 'Register', '新進報到')
    NewPosition = (5, 'New Position', '新職報到')
    TransferPosition = (6, 'Transfer Position', '調職')
    Retirement = (7, 'Retirement', '退伍')
    ChangeSoftCer = (8, 'Change Soft Certificate', '更換軟憑')
    BrokenReApply = (9, 'Broken Reapply', '卡片毀損，重新申請')


class ItemStatus(Enum):
    Available = (1, 'Available', '可用')
    Reserved = (2, 'Reserved', '預留')
    In_Transit = (3, 'In Transit', '在途')
    Damaged = (4, 'Damaged', '損耗')
    Picking = (5, 'Picking', '揀選中')
    In_Progress = (6, 'In Progress', '處理中')
    Delivered = (7, 'Delivered', '已送達')
    Returned = (0, 'Returned', '被退回')


class OrderStatus(Enum):
    Pending = (0, 'Pending', '待確認')
    Confirmed = (1, 'Confirmed', '已確認')
    Process = (2, 'Process', '處理中')
    Completed = (3, 'Completed', '已完成')
    Canceled = (4, 'Canceled', '已取消')
