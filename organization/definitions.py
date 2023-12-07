from enum import Enum


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
    SergeantMajor = (0x4F522D39, 'Sergeant Major', '一等士官長')
    FirstSergeant = (0x4F522D38, 'First Sergeant', '二等士官長')
    SergeantFirstClass = (0x4F522D37, 'Sergeant First Class', '三等士官長')
    StaffSergeant = (0x4F522D36, 'Staff Sergeant', '上士')
    Sergeant = (0x4F522D35, 'Sergeant', '中士')
    Corporal = (0x4F522D34, 'Corporal', '下士')
    PrivateFirstClass = (0x4F522D33, 'Private First Class', '上等兵')
    PrivateE2 = (0x4F522D32, 'Private E2', '一等兵')
    Private = (0x4F522D31, 'Private', '二等兵')


class CPC4Unit(Enum):
    NonSet = (000000, 'Non Set', '尚未設定')
    Headquarters = (804000, 'Headquarters', '隊本部')
    Duty_branch = (804930, 'Duty Branch', '勤務分隊')
    CIE_squad = (804012, 'CIE Squad', '通資小隊')   # CIE = Communication, Information and Electronic
    first_patrol_station = (704310, 'First Patrol Station', '第一機動巡邏站')
    second_patrol_station = (704320, 'Second Patrol Station', '第二機動巡邏站')
    XuCuoLiao_inspection_office = (704010, 'XuCuoLiao Inspection Office', '許厝寮安檢所')
    # 許厝寮安檢所
    MaiLiao_harbor_inspection_office = (704020, 'Mailiao Harbor Inspection Office', '麥寮工業港安檢所')
    # 麥寮工業港安檢所
    WenGang_inspection_office = (704030, 'WenGang Inspection Office', '蚊港安檢所')
    # 蚊港安檢所
    WuTiaoGang_fishing_harbor_inspection_office = (704040, 'WuTiaoGang Fishing Harbor Inspection Office', '五條港漁港安檢所')
    # 五條港漁港安檢所
    TaiXi_fishing_harbor_inspection_office = (704050, 'TaiXi Fishing Harbor Inspection Office', '台西漁港安檢所')
    # 台西漁港安檢所
    SanTiaoLu_fishing_harbor_inspection_office = (704060, 'SanTiaoLu Fishing Harbor Inspection Office', '三條崙漁港安檢所')
    # 三條崙漁港安檢所
    BoZiLiao_fishing_harbor_inspection_office = (704070, 'BoZiLiao Fishing Harbor Inspection Office', '箔子寮漁港安檢所')
    # 箔子寮漁港安檢所
    JinHu_fishing_harbor_inspection_office = (704080, 'JinHu Fishing Harbor Inspection Office', '金湖漁港安檢所')
    # 金湖漁港安檢所
    TaiZiVillage_fishing_harbor_inspection_office = (704090, 'TaiZiVillage Fishing Harbor Inspection Office', '台子村漁港安檢所')
    # 台子村漁港安檢所
    XiaHuKou_inspection_office = (704110, 'XiaHuKou Inspection Office', '下湖口安檢所')
    # 下湖口安檢所
    FuLai_fishing_harbor_inspection_office = (704210, 'FuLai Fishing Harbor Inspection Office', '副瀨漁港安檢所')
    # 副瀨漁港安檢所
    XingCuo_fishing_harbor_inspection_office = (704220, 'XingCuo Fishing Harbor Inspection Office', '型厝漁港安檢所')
    # 型厝漁港安檢所
    WenGang_fishing_harbor_inspection_office = (704230, 'WenGang Fishing Harbor Inspection Office', '塭港漁港安檢所')
    # 塭港漁港安檢所
    DongShi_fishing_harbor_inspection_office = (704240, 'DongShi Fishing Harbor Inspection Office', '東石漁港安檢所')
    # 東石漁港安檢所
    WangLiau_fishing_harbor_inspection_office = (704250, 'WangLiau Fishing Harbor Inspection Office', '網寮漁港安檢所')
    # 網寮漁港安檢所
    BaiShuiHu_fishing_harbor_inspection_office = (704260, 'BaiShuiHu Fishing Harbor Inspection Office', '白水湖漁港安檢所')
    # 白水湖漁港安檢所
    BuDai_fishing_port_inspection_office = (704270, 'BuDai Fishing Port Inspection Office', '布袋漁港安檢所')
    # 布袋漁港安檢所
    BuDai_port_inspection_office = (704280, 'BuDai Port Inspection Office', '布袋商港安檢所')
    # 布袋商港安檢所
    HauMeiVillage_fishing_harbor_inspection_office = (704290, 'HauMeiVillage Fishing Harbor Inspection Office', '好美里漁港安檢所')
    # 好美里漁港安檢所
