## REST
### Лёгкая нагрузка (sanity check): убедиться, что всё работает.
Запустить приложение со следуюшими ресурсами:
```
docker run -p 8000:8000 --cpus="0.708" --memory="133M" -d app_http
```
Запустить нагрузку и после установить символическое число пользователей (например, 5 на 30с)
1. `locust -f tests/performance/rest/locustfile.py`
2.  Перейти по адресу: `http://localhost:8089`

Убедиться, что все отработало успешно

<img width="2612" height="1800" alt="total_requests_per_second_1768743696 912" src="https://github.com/user-attachments/assets/70efdf85-940a-4646-b49f-fb7b79ca81f9" />

### Установка рабочей нагрузки
В качестве рабочей нагрузки было принято значение в 280 rps для установленных ранее ресурсов


<img width="2928" height="1800" alt="total_requests_per_second_1768744392 496" src="https://github.com/user-attachments/assets/877da63f-e866-47a6-bfee-6c7c2b816304" />


Характеристики системы в момент рабочей нагрузки

<img width="1223" height="593" alt="Снимок экрана 2026-01-18 в 16 49 50" src="https://github.com/user-attachments/assets/2c19e341-b8cd-41e2-bb8f-833074743b8a" />

### Стресс-тест (приближение к пику): выявить пределы производительности.

Постепенно увеличим количество пользователей до наступления момента пика (900 пользователей)



Графики перед наступлением пика (видно, что начинается нехватка ресурсов)

<img width="1233" height="768" alt="Снимок экрана 2026-01-09 в 13 08 58" src="https://github.com/user-attachments/assets/db8515b9-33ba-4116-9c7c-55fb7cbd947a" />

### Тест на стабильность
В качестве проверки было взято значение приближенное к пику (800 пользователей, 455 rps)

<img width="2928" height="1800" alt="total_requests_per_second_1768746677 338" src="https://github.com/user-attachments/assets/743ca1a9-2fcf-4bb5-aed4-02cc2aff89b9" />


Заметны скачки по времени ответа а также потребления памяти при длительной нагрузке на значениях близких к пиковой нагрузке, но система еще справляется

<img width="1223" height="593" alt="Снимок экрана 2026-01-18 в 17 23 55" src="https://github.com/user-attachments/assets/5c0c54a8-6abd-49c6-a55c-51ff72ed1c25" />

