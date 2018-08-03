from splinter import Browser
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--log-level=3')

host = "http://88.99.2.149:"
port = "4242"
url = host + port


# driver = webdriver.Chrome("C:/Chromedriver/chromedriver.exe")
browser = Browser("chrome")
browser.visit(f"{url}/furnace/concentrate_report_journal")
if browser.is_element_present_by_id("loginform", 2):
    browser.fill("username", "inframine")
    browser.fill("password", "Singapore2017")
    browser.find_by_css("input.btn").click()
#ОБЖИГ
#Журнал рапортов о проделанной работе по складам концентратов

if browser.is_element_present_by_id("table_id_big_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_1.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_1.png")
    print("Обжиг->Рапорта по складам->Учет поставок Some wrong!")

if browser.is_element_present_by_id("table_id_upper_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_2.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_2.png")
    print("Обжиг->Рапорта по складам->Ответственные по складу Some wrong!")

if browser.is_element_present_by_id("table_id_small_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_3.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_3.png")
    print("Обжиг->Рапорта по складам->Разгружено/остаток Some wrong!")

#Журнал рапортов ОЦ

browser.visit(f"{url}/furnace/reports_furnace_area")
if browser.is_element_present_by_id("table_id_self_protection_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_4.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_4.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Самоохрана Some wrong!")

if browser.is_element_present_by_id("table_id_fences_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_5.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_5.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Ограждения Some wrong!")

if browser.is_element_present_by_id("table_id_airmachines", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_6.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_6.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Участок воздуходувных машин Some wrong!")

if browser.is_element_present_by_id("table_id_corrective_actions_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_7.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_7.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Корректирующие действия Some wrong!")

if browser.is_element_present_by_id("table_id_udel_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_8.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_8.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Удельная производительность печей Some wrong!")


if browser.is_element_present_by_id("table_id_concentration_by_time_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_9.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_9.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Концентрация по времени Some wrong!")

if browser.is_element_present_by_id("table_id_worth_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_10.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_10.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Мат. Тех. Ценности Some wrong!")

if browser.is_element_present_by_id("table_id_area_class_cinder", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_11.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_11.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Участок классификации огарка Some wrong!")

if browser.is_element_present_by_id("table_id_electrofilter", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_12.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_12.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Участок электрофильтров Some wrong!")

if browser.is_element_present_by_id("table_id_places_of_sampling_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_13.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_13.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Места отбора пробы Some wrong!")

if browser.is_element_present_by_id("table_id_warehouse_concentrates", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_14.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_14.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Склад концентратов Some wrong!")

if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_15.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_15.png")
    print("Обжиг->Журнал рапортов ОЦ->Журнал рапортов ОЦ->Печной участок Some wrong!")

#Поступление, расходы и остатки Zn концентратов

browser.visit(f"{url}/furnace/report_income_outcome_schieht")
if browser.is_element_present_by_id("table_id_summary_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_16.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_16.png")
    print("Обжиг->Журнал рапортов ОЦ->Постпление расходы и остатки Zn концентратов->НЗП и склады Some wrong!")

if browser.is_element_present_by_id("table_id_year_plan_schieht", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_17.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_17.png")
    print("Обжиг->Журнал рапортов ОЦ->Постпление расходы и остатки Zn концентратов->Расчет годового плана шихты Some wrong!")

if browser.is_element_present_by_id("table_id_small_plan_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_18.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_18.png")
    print("Обжиг->Журнал рапортов ОЦ->Постпление расходы и остатки Zn концентратов->Какая-то таблица Some wrong!")

if browser.is_element_present_by_id("table_id_supply_of_zinc_concentrates", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_19.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_19.png")
    print("Обжиг->Журнал рапортов ОЦ->Постпление расходы и остатки Zn концентратов->Поставка цинковых концентратов Some wrong!")

if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_20.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_20.png")
    print("Обжиг->Журнал рапортов ОЦ->Постпление расходы и остатки Zn концентратов->Поступление расходы и остатки Zn концентратов Some wrong!")

#Расчет металлов

browser.visit(f"{url}/furnace/metals_compute")
if browser.is_element_present_by_id("table_id_sgok_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_21.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_21.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->СГОК таблица Some wrong!")

if browser.is_element_present_by_id("table_id_contain_zn_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_22.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_22.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->Содержание в Some wrong!")

if browser.is_element_present_by_id("table_id_sns_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_23.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_23.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->СНС Some wrong!")

if browser.is_element_present_by_id("table_id_concentrat_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_24.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_24.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->Концентрат Some wrong!")

if browser.is_element_present_by_id("table_id_gof_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_25.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_25.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->ГОФ таблица Some wrong!")

if browser.is_element_present_by_id("table_id_avg_month_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_26.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_26.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->Среднее содержание за месяц Some wrong!")

if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_27.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_27.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->Среднее содержание за месяц Some wrong!")

if browser.is_element_present_by_id("table_id_cinder_conc_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_28.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_28.png")
    print("Обжиг->Журнал рапортов ОЦ->Расчет металлов->Огарок Some wrong!")

#Журнал сменных производственных техзаданий

browser.visit(f"{url}/furnace/technological_tasks")
if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_29.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_29.png")
    print("Обжиг->Журнал сменных производственных техзаданий->Технологические задания Some wrong!")

#Журнал по ремонту (ОЦ)

browser.visit(f"{url}/furnace/furnace_repair")
if browser.is_element_present_by_id("table_id_repair_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_30.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_30.png")
    print("Обжиг->Журнал по ремонту->Ремонты по обжиговому цеху Some wrong!")

#Рабочий журнал изменения фракции

browser.visit(f"{url}/furnace/furnace_changed_fraction")
if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_31.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_31.png")
    print("Обжиг->Рабочий журнал изменения фракции->Изменение фракции Some wrong!")

#ВЫЩЕЛАЧИВАНИЕ
#Журнал экспресс-анализа

browser.visit(f"{url}/leaching/leaching_express_analysis")
if browser.is_element_present_by_id("table_id_neutral_thickeners_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_32.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_32.png")
    print("Выщелачивание->Журнал экспресс-анализа->Нейтральные сгустители Some wrong!")

if browser.is_element_present_by_id("table_id_tanks_for_finished_products_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_33.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_33.png")
    print("Выщелачивание->Журнал экспресс-анализа->Баки готовой продукции Some wrong!")

if browser.is_element_present_by_id("table_id_reagents_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_34.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_34.png")
    print("Выщелачивание->Журнал экспресс-анализа->Реагенты Some wrong!")

if browser.is_element_present_by_id("table_id_self_protection_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_35.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_35.png")
    print("Выщелачивание->Журнал экспресс-анализа->Самоохрана Some wrong!")

if browser.is_element_present_by_id("table_id_shift_info_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_36.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_36.png")
    print("Выщелачивание->Журнал экспресс-анализа->Смена Some wrong!")

if browser.is_element_present_by_id("table_id_agitators_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_37.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_37.png")
    print("Выщелачивание->Журнал экспресс-анализа->Агитаторы очистки Some wrong!")

if browser.is_element_present_by_id("table_id_zinc_pulp_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_38.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_38.png")
    print("Выщелачивание->Журнал экспресс-анализа->Цинковая пульпа Some wrong!")

if browser.is_element_present_by_id("table_id_cinder_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_39.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_39.png")
    print("Выщелачивание->Журнал экспресс-анализа->Огарок Some wrong!")

if browser.is_element_present_by_id("table_id_thickeners_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_40.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_40.png")
    print("Выщелачивание->Журнал экспресс-анализа->Сгустители Some wrong!")

if browser.is_element_present_by_id("table_id_loads_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_41.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_41.png")
    print("Выщелачивание->Журнал экспресс-анализа->Нагрузки Some wrong!")

if browser.is_element_present_by_id("table_id_neutral_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_42.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_42.png")
    print("Выщелачивание->Журнал экспресс-анализа->Нейтральный р-р Some wrong!")

if browser.is_element_present_by_id("table_id_vsns_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_43.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_43.png")
    print("Выщелачивание->Журнал экспресс-анализа->ВСНС Some wrong!")

if browser.is_element_present_by_id("table_id_tanks_availability_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_44.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_44.png")
    print("Выщелачивание->Журнал экспресс-анализа->Свободные емкости Some wrong!")

if browser.is_element_present_by_id("table_id_schieht_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_45.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_45.png")
    print("Выщелачивание->Журнал экспресс-анализа->Шихта Some wrong!")

if browser.is_element_present_by_id("table_id_appt_hydrometal_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_46.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_46.png")
    print("Выщелачивание->Журнал экспресс-анализа->Аппаратчик-гидрометаллург Some wrong!")

if browser.is_element_present_by_id("table_id_sample_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_47.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_47.png")
    print("Выщелачивание->Журнал экспресс-анализа->Пробник Some wrong!")

#Журнал по ремонту оборудования ЦВЦО

browser.visit(f"{url}/leaching/leaching_repair_quipment")
if browser.is_element_present_by_id("table_id_repair_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_48.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_48.png")
    print("Выщелачивание->Журнал ремонтов Some wrong!")

#ЭЛЕКТРОЛИЗ
#Журнал по ремонту оборудования

browser.visit(f"{url}/electrolysis/electrolysis_repair_report_tables")
if browser.is_element_present_by_id("table_id_main_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_49.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_49.png")
    print("Электролиз->Журнал по ремонту оборудования Some wrong!")

#Журнал рапортов мастеров смен

browser.visit(f"{url}/electrolysis/masters_raports")
if browser.is_element_present_by_id("table_id_last_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_50.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_50.png")
    print("Электролиз->Журнал рапортов мастеров смен->Последняя тамблица Some wrong!")

if browser.is_element_present_by_id("table_id_melt_area1", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_51.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_51.png")
    print("Электролиз->Журнал рапортов мастеров смен->Плавильный участок-1 Some wrong!")

if browser.is_element_present_by_id("table_id_melt_area2", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_52.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_52.png")
    print("Электролиз->Журнал рапортов мастеров смен->Плавильный участок-2 Some wrong!")

if browser.is_element_present_by_id("table_id_params_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_53.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_53.png")
    print("Электролиз->Журнал рапортов мастеров смен->Параметры Some wrong!")

if browser.is_element_present_by_id("table_id_zinc_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_54.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_54.png")
    print("Электролиз->Журнал рапортов мастеров смен->Цинк товарный Some wrong!")

if browser.is_element_present_by_id("table_id_seria3_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_55.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_55.png")
    print("Электролиз->Журнал рапортов мастеров смен->3-я серия Some wrong!")

if browser.is_element_present_by_id("table_id_seria1_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_56.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_56.png")
    print("Электролиз->Журнал рапортов мастеров смен->1-я 2-я серия Some wrong!")

if browser.is_element_present_by_id("table_id_seria4_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_57.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_57.png")
    print("Электролиз->Журнал рапортов мастеров смен->4-я серия Some wrong!")

#Технологические журналы 1-й и 2-й серии

browser.visit(f"{url}/electrolysis/electrolysis_technical_report_12_degree")
if browser.is_element_present_by_id("table_id_left_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_58.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_58.png")
    print("Электролиз->Технологические журналы 1-й и 2-й серии->Время замеров и работа оборудования Some wrong!")

if browser.is_element_present_by_id("table_id_right_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_59.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_59.png")
    print("Электролиз->Технологические журналы 1-й и 2-й серии->Технологический режим, ПАВ и кристаллизаторы Some wrong!")

#Технологический журнал электролиза 3-й серии

browser.visit(f"{url}/electrolysis/electrolysis_technical_report_3_degree")
if browser.is_element_present_by_id("table_id_left_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_60.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_60.png")
    print("Электролиз->Технологические журналы 3-й серии->Время замеров и работа оборудования Some wrong!")

if browser.is_element_present_by_id("table_id_right_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_61.png")

else:
    browser.driver.save_screenshot("screens/screenshot_errors_61.png")
    print("Электролиз->Технологические журналы 3-й серии->Технологический режим, ПАВ и кристаллизаторы Some wrong!")

#ТЕхнологический журнал электролиза 4-й серии

browser.visit(f"{url}/electrolysis/electrolysis_technical_report_4_degree")
if browser.is_element_present_by_id("table_id_left_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_62.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_62.png")
    print("Электролиз->Технологические журналы 4-й серии->Время замеров и работа оборудования Some wrong!")

if browser.is_element_present_by_id("table_id_right_table", 2):
    browser.driver.save_screenshot("screens/screenshot_all_ok_63.png")
    print("All OK")
else:
    browser.driver.save_screenshot("screens/screenshot_errors_63.png")
    print("Электролиз->Технологические журналы 4-й серии->Технологический режим, ПАВ и кристаллизаторы Some wrong!")

# if browser.is_element_present_by_css(".vdatetime .from-control", 2):
#    browser.find_by_css(".vdatetime .from-control").click()
#    browser.driver.save_screenshot("screens/screenshot1.png")
#        browser.find_by_css("vdatetime-popup__actions__button").click()


# if browser.is_element_present_by_id("table_id_loads_table", 2):
#    browser.driver.save_screenshot("screens/screenshot.png")
#    print("All OK")
# else:
#    browser.driver.save_screenshot("screens/errors.png")
#    print("Some wrong!")

browser.quit()#
