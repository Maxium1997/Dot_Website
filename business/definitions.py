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
