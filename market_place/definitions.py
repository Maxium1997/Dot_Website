from enum import Enum


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
