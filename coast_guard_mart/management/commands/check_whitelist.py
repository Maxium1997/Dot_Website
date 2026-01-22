# coast_guard_mart/management/commands/check_whitelist.py
from django.core.management.base import BaseCommand
from coast_guard_mart.models import WhitelistMember
from organization.models import Unit


class Command(BaseCommand):
    help = '檢查白名單成員的單位層級一致性'

    def handle(self, *args, **options):
        members = WhitelistMember.objects.all()
        self.stdout.write(self.style.SUCCESS(f"開始檢查 {members.count()} 筆白名單資料..."))

        error_count = 0
        for member in members:
            unit = member.unit
            depth = 1
            temp_unit = unit

            # 計算該單位所在的深度
            while temp_unit.superior:
                depth += 1
                temp_unit = temp_unit.superior

            # 輸出檢查結果
            if depth < 5:
                # 取得下級單位數量
                sub_count = Unit.objects.filter(
                    superior_content_type__model='unit',
                    superior_object_id=unit.id
                ).count()

                if sub_count > 0:
                    self.stdout.write(self.style.WARNING(
                        f"警告: [{member.name}] 登記在第 {depth} 層 ({unit.name})，"
                        f"但該單位還有 {sub_count} 個下級單位。使用者可能會選到更深層導致核對失敗。"
                    ))
                    error_count += 1

        if error_count == 0:
            self.stdout.write(self.style.SUCCESS("檢查完成：所有白名單成員均登記在最底層單位。"))
        else:
            self.stdout.write(self.style.ERROR(f"檢查完成：共發現 {error_count} 筆潛在不一致資料。"))