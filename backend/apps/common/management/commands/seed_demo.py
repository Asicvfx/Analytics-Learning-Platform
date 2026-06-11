"""Seed the catalog: categories (applications), reports, and learning materials.

The catalog content lives in code (authoritative). Reports are external links
(Qlik Sense / web tools / Telegram bots) shown as cards with a description,
an "open report" button, learning materials and an FAQ.

Usage:
  seed_demo                 seed (adds missing items)
  seed_demo --if-empty      skip entirely if categories already exist
  seed_demo --reseed        wipe the catalog (categories/dashboards/sheets/
                            widgets/learning/permissions) and rebuild it,
                            preserving users, roles and audit logs.

Note: qtest/Qlik and 10.x links are internal corporate resources and open only
from the corporate network/VPN.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Role
from apps.categories.models import Category
from apps.dashboards.models import Dashboard, DashboardPermission
from apps.learning.models import LearningMaterial
from apps.sheets.models import DashboardSheet
from apps.widgets.models import DashboardWidget

User = get_user_model()

# --- Support contacts (BI department), appended to instructions ---
SUPPORT = (
    "\n\nПоддержка — Отдел BI:\n"
    "• Баймбетова Гульмира — +7 702 752 3253\n"
    "• Бекбаева Нургуль — 8 (7142) 573-419, +7 702 703 7171\n"
    "• Тамырбаев Даурен — +7 747 746 5015"
)

# --- Shared Qlik navigation FAQ ---
SHARED_FAQ = [
    {"question": "Навигация между листами",
     "answer": "Используйте кнопку навигации сверху справа, чтобы открыть "
               "список всех листов отчёта, либо щёлкайте по стрелкам "
               "«вперёд»/«назад» для перехода между листами."},
    {"question": "Как экспортировать данные",
     "answer": "Щёлкните правой кнопкой мыши по таблице → «Загрузить как…» → "
               "«Данные» → включите «Форматирование таблицы» → «Экспорт». Если "
               "файл не появился, проверьте вкладку «Загрузки» в браузере."},
    {"question": "Как сохранить отчёт",
     "answer": "Следуйте инструкции по экспорту данных — выгрузите нужную "
               "таблицу в Excel."},
    {"question": "Как изменить порядок столбцов",
     "answer": "Перетащите заголовки столбцов в нужном порядке."},
    {"question": "Как искать значения",
     "answer": "Используйте значок лупы рядом с полями для поиска и фильтрации."},
]

# --- Instruction texts ---
FLAGSHIP_CONTENT = (
    "Цель отчёта: представление оперативных данных для анализа "
    "производительности и эффективности.\n\n"
    "Доступ: перейдите по ссылке и войдите, используя логин и пароль от "
    "вашего аккаунта CDN.\n\n"
    "Основные разделы (листы):\n"
    "• «Новые установки / Отток» — динамика новых установок и оттока.\n"
    "• «Доходы» — доход в разрезе макрорегионов, услуг и сегментов.\n\n"
    "Настройка фильтров:\n"
    "Фильтровать данные можно по полям со значком лупы. Доступные фильтры: "
    "Тип заказа, Макрорегион, Услуга, Филиал, Сегмент, Отчётный период. "
    "Выберите значения и нажмите зелёную галочку, чтобы применить; красный "
    "крестик или Esc — отмена. Для диапазона дат используйте символы "
    ">=, <=, >, < в поле «Дата заказа».\n\n"
    "Экспорт в Excel:\n"
    "ПКМ по таблице → «Загрузить как…» → «Данные» → включить «Форматирование "
    "таблицы» → «Экспорт».\n\n"
    "Примеры использования: анализ по новым установкам; анализ по оттоку; "
    "выгрузка по макрорегиону/филиалу/сегменту; выгрузка в разрезе услуг; "
    "выгрузка по типу заказа; выгрузка по эффективности менеджеров." + SUPPORT
)

STANDARD_CONTENT = (
    "Откройте отчёт по кнопке выше и войдите, используя логин и пароль от "
    "вашего аккаунта CDN.\n"
    "Используйте фильтры (поля со значком лупы) для выбора периода, региона и "
    "других параметров: зелёная галочка — применить, Esc — отмена.\n"
    "Экспорт: ПКМ по таблице → «Загрузить как…» → «Данные» → «Форматирование "
    "таблицы» → «Экспорт»." + SUPPORT
)

MVP_AGENT_CONTENT = (
    "MVP ИИ-агент помогает автоматизировать анализ и обработку технических "
    "спецификаций (ТЗ) в государственных закупках:\n"
    "• извлечение ключевой информации из лотов и технических документов;\n"
    "• аналитика по участникам торгов (например, по БИН организаций);\n"
    "• рекомендации по участию и стратегии ставок на основе истории участия "
    "и побед;\n"
    "• мониторинг цен, медианных разрывов и узких проигрышей;\n"
    "• отчёты о конкурентах и динамике торгов.\n\n"
    "Точки доступа:\n"
    "• Веб: http://10.8.36.60:8501/ (резерв: http://10.71.76.202:8501/)\n"
    "• Телеграм-бот: @goszakup_ai_KTbot\n\n"
    "Примечание: ресурсы доступны из корпоративной сети."
)

SPEEDTEST_CONTENT = (
    "Карта отображает провайдеров и качество их интернета в Казахстане на "
    "основе данных SpeedTest.\n"
    "Откройте веб-приложение по кнопке выше (доступно из корпоративной сети)."
)

SALESHELPER_CONTENT = (
    "SalesHelper Bot оптимизирует и автоматизирует расчёт тарифов и генерацию "
    "коммерческих предложений.\n"
    "Откройте бота в Telegram (@kazakht_test_bot) и следуйте подсказкам."
)

# (name, slug, description, icon, order)
CATEGORIES = [
    ("Доход", "dohod",
     "Дашборды по доходу, новым установкам и оттоку.", "chart-line", 1),
    ("Заказы", "zakazy",
     "Аналитика по заказам клиентов (CRM 2.0).", "shopping-cart", 2),
    ("Контакты", "kontakty",
     "Контактные данные действующих юридических лиц.", "phone", 3),
    ("БИН-ы", "biny",
     "Аналитика по БИН организаций.", "building", 4),
    ("Объекты образования и здравоохранения", "obrazovanie-zdravoohranenie",
     "Детализированные данные по объектам образования и здравоохранения.",
     "hospital", 5),
    ("ИИ-инструменты", "ai-instrumenty",
     "ИИ-агенты и инструменты автоматизации.", "cpu", 6),
]

# Each report: title, slug, category_slug, kind, url, access, tags,
# description, learning (content/video/presentation/faq).
DASHBOARDS = [
    {
        "title": "Оперативный Дашборд по Макрорегионам",
        "slug": "operativnyy-dashbord-makroregiony",
        "category": "dohod", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "bffa967b-f9b9-4e63-85e0-133930f982de/overview",
        "access": Dashboard.EMPLOYEE,
        "tags": ["доход", "макрорегионы", "отток", "установки"],
        "description": "Ключевые показатели периода: доход, новые заявки на "
                       "установки и отток по оперативным данным.",
        "content": FLAGSHIP_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "Общая детализация 2 спец v2",
        "slug": "obshchaya-detalizaciya-2-spec-v2",
        "category": "dohod", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "f4d2eef3-d664-4273-869f-150d357c5d78/overview",
        "access": Dashboard.EMPLOYEE,
        "tags": ["детализация", "отчётный период"],
        "description": "Детализированные данные за указанный отчётный период.",
        "content": STANDARD_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "Заказы CRM 2.0",
        "slug": "zakazy-crm-2-0",
        "category": "zakazy", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "049ee791-de65-4047-847e-76482333ef58/overview",
        "access": Dashboard.EMPLOYEE,
        "tags": ["заказы", "crm", "детализация"],
        "description": "Представление детализированных данных по всем заказам.",
        "content": STANDARD_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "Контактные данные юридических лиц (CRM 2.0)",
        "slug": "kontaktnye-dannye-crm-2-0",
        "category": "kontakty", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "48ac9ee8-e738-49c0-83fc-ca9eba11df8a/overview",
        "access": Dashboard.MANAGER,
        "tags": ["контакты", "юрлица", "crm"],
        "description": "Контактные данные действующих юридических лиц из "
                       "системы CRM 2.0.",
        "content": STANDARD_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "Дашборд БИН-ы 2026",
        "slug": "dashbord-biny-2026",
        "category": "biny", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "c9270bac-0f62-4b76-b727-04618908415c/overview",
        "access": Dashboard.MANAGER,
        "tags": ["бин", "организации"],
        "description": "Содержит полную информацию по БИН организаций.",
        "content": STANDARD_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "Дашборд по объектам образования и здравоохранения",
        "slug": "obekty-obrazovaniya-zdravoohraneniya",
        "category": "obrazovanie-zdravoohranenie", "kind": Dashboard.QLIK,
        "url": "https://qtest/sense/app/"
               "c51f54cb-8f1b-458a-aaa3-a27b95a9f08f/overview",
        "access": Dashboard.EMPLOYEE,
        "tags": ["образование", "здравоохранение", "объекты"],
        "description": "Детализированные данные по объектам образования и "
                       "здравоохранения.",
        "content": STANDARD_CONTENT, "faq": SHARED_FAQ,
    },
    {
        "title": "MVP ИИ-агент для госзакупок",
        "slug": "mvp-ii-agent-goszakupki",
        "category": "ai-instrumenty", "kind": Dashboard.WEB,
        "url": "http://10.8.36.60:8501/",
        "access": Dashboard.EMPLOYEE,
        "tags": ["ии", "госзакупки", "тз", "агент"],
        "description": "ИИ-агент для автоматизации анализа технических "
                       "спецификаций и аналитики по госзакупкам.",
        "content": MVP_AGENT_CONTENT, "faq": [],
    },
    {
        "title": "Карта провайдеров (SpeedTest)",
        "slug": "karta-provayderov-speedtest",
        "category": "ai-instrumenty", "kind": Dashboard.WEB,
        "url": "http://10.8.36.60:5174/",
        "access": Dashboard.EMPLOYEE,
        "tags": ["провайдеры", "speedtest", "карта"],
        "description": "Карта провайдеров и качества интернета в Казахстане на "
                       "основе данных SpeedTest.",
        "content": SPEEDTEST_CONTENT, "faq": [],
    },
    {
        "title": "SalesHelper Bot",
        "slug": "saleshelper-bot",
        "category": "ai-instrumenty", "kind": Dashboard.BOT,
        "url": "https://t.me/kazakht_test_bot",
        "access": Dashboard.EMPLOYEE,
        "tags": ["продажи", "тарифы", "бот"],
        "description": "Инструмент для оптимизации расчёта тарифов и генерации "
                       "коммерческих предложений.",
        "content": SALESHELPER_CONTENT, "faq": [],
    },
]

PERMISSIONS = [
    # role_name, can_view, can_export, can_edit
    (Role.ADMIN, False, True, True),
    (Role.ANALYST, False, True, True),
    (Role.MANAGER, False, True, False),
    (Role.EMPLOYEE, False, True, False),
]


class Command(BaseCommand):
    help = "Seed the catalog (categories, reports, learning materials)."

    def add_arguments(self, parser):
        parser.add_argument("--if-empty", action="store_true",
                            help="Skip seeding if categories already exist.")
        parser.add_argument("--reseed", action="store_true",
                            help="Wipe and rebuild the catalog (keeps users).")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["if_empty"] and Category.objects.exists():
            self.stdout.write("Data already present — skipping seed.")
            return

        self._seed_roles_and_users()

        if options["reseed"]:
            self._wipe_catalog()

        categories = self._seed_categories()
        self._seed_dashboards(categories)
        self.stdout.write(self.style.SUCCESS("Catalog seeded successfully."))

    # --- wipe catalog (preserve users/roles/audit) ---
    def _wipe_catalog(self):
        LearningMaterial.objects.all().delete()
        DashboardWidget.objects.all().delete()
        DashboardSheet.objects.all().delete()
        DashboardPermission.objects.all().delete()
        Dashboard.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Catalog wiped for reseed.")

    # --- roles & users ---
    def _seed_roles_and_users(self):
        for name in [Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.EMPLOYEE]:
            Role.objects.get_or_create(name=name)

        demo_users = [
            ("Demo Admin", "admin@example.com", "admin123", Role.ADMIN,
             "Analytics", "Administrator"),
            ("Demo Analyst", "analyst@example.com", "analyst123", Role.ANALYST,
             "Analytics", "Analyst"),
            ("Demo Manager", "manager@example.com", "manager123", Role.MANAGER,
             "Sales", "Manager"),
            ("Demo Employee", "employee@example.com", "employee123",
             Role.EMPLOYEE, "Operations", "Specialist"),
        ]
        for full_name, email, password, role, dept, position in demo_users:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"full_name": full_name, "department": dept,
                          "position": position,
                          "is_staff": role == Role.ADMIN,
                          "is_superuser": role == Role.ADMIN},
            )
            if created:
                user.set_password(password)
                user.save()
            user.roles.set([Role.objects.get(name=role)])

    # --- categories ---
    def _seed_categories(self):
        result = {}
        for name, slug, desc, icon, order in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": desc, "icon": icon,
                          "display_order": order},
            )
            result[slug] = cat
        return result

    # --- dashboards (reports) + permissions + learning ---
    def _seed_dashboards(self, categories):
        admin = User.objects.filter(email="admin@example.com").first()
        for item in DASHBOARDS:
            dash, created = Dashboard.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "category": categories[item["category"]],
                    "title": item["title"],
                    "description": item["description"],
                    "report_url": item["url"],
                    "report_kind": item["kind"],
                    "business_purpose": item["description"],
                    "owner_name": "Отдел BI",
                    "access_level": item["access"],
                    "status": Dashboard.PUBLISHED,
                    "tags": ", ".join(item["tags"]),
                    "last_updated_at": timezone.now(),
                    "created_by": admin,
                },
            )
            if not created:
                continue
            for role_name, cv, ce, ced in PERMISSIONS:
                DashboardPermission.objects.create(
                    dashboard=dash, role_name=role_name,
                    can_view=cv, can_export=ce, can_edit=ced,
                )
            LearningMaterial.objects.create(
                dashboard=dash,
                title=f"Инструкция: {item['title']}",
                content=item["content"],
                video_url="",
                presentation_url="",
                faq_json=item["faq"],
                created_by=admin,
            )
