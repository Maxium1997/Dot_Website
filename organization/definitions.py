from enum import Enum


class Classification(Enum):
    Headquarters = (0, 'Headquarters', '本部')
    First = (1, 'First', '第一')
    Second = (2, 'Second', '第二')
    Third = (3, 'Third', '第三')
    Forth = (4, 'Forth', '第四')
    Fifth = (5, 'Fifth', '第五')
    Sixth = (6, 'Sixth', '第六')
    Seventh = (7, 'Seventh', '第七')
    Eighth = (8, 'Eighth', '第八')
    Ninth = (9, 'Ninth', '第九')
    Tenth = (10, 'Tenth', '第十')
    Eleventh = (11, 'Eleventh', '第十一')
    Twelfth = (12, 'Twelfth', '第十二')
    Thirteenth = (13, 'Thirteenth', '第十三')


class ArmyCommission(Enum):
    NonSet = (0x4E6F4E, 'Non Set', '尚未設定')
    General = (0x4F462D39, 'General', '上將')
    LieutenantGeneral = (0x4F462D38, 'Lieutenant General', '中將')
    MajorGeneral = (0x4F462D37, 'Major General', '少將')
    Colonel = (0x4F462D35, 'Colonel', '上校')
    LieutenantColonel = (0x4F462D34, 'Lieutenant Colonel', '中校')
    Major = (0x4F462D33, 'Major', '少校')
    Captain = (0x4F462D32, 'Captain', '上尉')
    FirstLieutenant = (0x4F462D31, 'First Lieutenant', '中尉')
    SecondLieutenant = (0x4F46, 'Second Lieutenant', '少尉')
    SergeantMajor = (0x4F522D39, 'Sergeant Major', '士官長')      # 一等士官長
    FirstSergeant = (0x4F522D38, 'First Sergeant', '士官長')      # 二等士官長
    SergeantFirstClass = (0x4F522D37, 'Sergeant First Class', '士官長')       # 三等士官長
    StaffSergeant = (0x4F522D36, 'Staff Sergeant', '上士')
    Sergeant = (0x4F522D35, 'Sergeant', '中士')
    Corporal = (0x4F522D34, 'Corporal', '下士')
    PrivateFirstClass = (0x4F522D33, 'Private First Class', '上等兵')
    PrivateE2 = (0x4F522D32, 'Private E2', '一等兵')
    Private = (0x4F522D31, 'Private', '二等兵')

