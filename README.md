# EveTycoon API
Документация API:  https://evetycoon.com/docs


## 1. Краткая информация

Бот призван помогать игрокам-добытчикам и промышленникам покупать и продавать базовые минералы (всего их 8 шт.). 
Ресурсы продаются на станциях, расположенных в звёздных системах, которые в свою очередь входят в один из 23 регионов, 
принадлежащих одной из 4 империй (+ их протектораты). Системы также делятся на безопасные (highsec – от high security), 
небезопасные (lowsec) и опасные (nullsec), что важно для выдачи результатов.


## 2. Список команд

### /help
Вывод списка и описание команд.

### /stats
Выводить статистику рынка. Статистика включает в себя: 

- объём покупок и продаж (в единицах минералов); 
- количество заказов (ордеров) на покупку товаров;
- количество ордеров на продажу товаров;
- минимальная цена покупки;
- максимальная цена продажи;
- средняя цена покупки;
- средняя цена продажи.

После выбора данной команды пользователь указывает товар - соответствующий минерал, статистику по которому 
желает получить (кнопки): Tritanium, Pyerite, Mexallon, Isogen, Nocxium, Zydrine, Megacyte, Morphite.

Далее указывает фильтры (кнопки):
- /all – топ 5 регионов по кол-ву сделок среди всех империй;
- /empire – топ 5 регионов в империях Amarr Empire, Khanid Kingdom и Ammatar Mandate;
- /state – топ 5 регионов в империи Caldari State;
- /federation – топ 5 регионов в империи Gallente Federation;
- /republic – топ 5 регионов в империи Minmatar Republic;


### /wtb (want to buy)
Выводит топ 5 предложений продажи в указанном регионе. Ответ содержит следующие данные:
- дата заказа; 
- продолжительность в днях;
- цена за единицу товара; 
- количество товара; 
- минимальное количество;
- регион;
- система; 
- станция.  

Выбор товара и фильтры аналогичны команде **/stats**

Далее пользователь указывает дополнительные параметры(кнопками):
- /highsec - только безопасные системы;
- /lowsecs - безопасные и небезопасные системы
- /all - все системы.


### /wts (want to sell)
Выводит топ 5 предложений покупки в указанном регионе. Ответ содержит аналогичные данные, что и команда **/wtb**.

Выбор товара и фильтры аналогичны команде **/stats**.

Дополнительные параметры аналогичны команде **/wtb**.

### /history

Выводит 5 последних команд пользователя с возможностью их повторить и получить актуальные данные.
В качестве ответа пользователь получает список команд и кнопки от 1 до 5 + отмена.


## 3. Вызовы API

Базовый адрес для всех запросов: https://evetycoon.com/api/v1/market/

### Команда **/stats** использует следующий запрос:

`/stats/{regionId}/{typeId}`

Пример запроса: https://evetycoon.com/api/v1/market/stats/10000002/34

Ответ:

```
{
  "buyVolume": 5736853583,
  "sellVolume": 10109935983,
  "buyOrders": 84,
  "sellOrders": 112,
  "buyOutliers": 2,
  "sellOutliers": 2,
  "buyThreshold": 0.49,
  "sellThreshold": 50.9,
  "buyAvgFivePercent": 4.84798363405329,
  "sellAvgFivePercent": 5.2113237080038,
  "maxBuy": 4.9,
  "minSell": 5.09
}
```


### Команды **\wtb** и **\wts** используют следующий запрос:

`orders/{typeId}?regionId={regionId}`

Пример запроса: https://evetycoon.com/api/v1/market/orders/34?regionId=10000002

Ответ состоит из пяти частей. Все они представлены ниже:

```
{
  "itemType": {
    "typeID": 34,
    "groupID": 18,
    "typeName": "Tritanium",
    "iconID": 22,
    "marketGroupID": 1857,
    "description": "The main building block in space structures. A very hard, yet bendable metal. Cannot be used in human habitats due to its instability at atmospheric temperatures. Very common throughout the central regions of known universe.\r\n\r\nMay be obtained by reprocessing the following ores and their variations available in high security status star systems:\r\n\u003Ca href=showinfo:1230\u003EVeldspar\u003C/a\u003E, \u003Ca href=showinfo:1228\u003EScordite\u003C/a\u003E, \u003Ca href=showinfo:18\u003EPlagioclase\u003C/a\u003E\r\n\r\nIt is also present in huge amounts in rare ores like \u003Ca href=showinfo:19\u003ESpodumain\u003C/a\u003E, \u003Ca href=showinfo:52316\u003EBezdnacine\u003C/a\u003E, \u003Ca href=showinfo:52315\u003ERakovene\u003C/a\u003E and \u003Ca href=showinfo:52306\u003ETalassonite\u003C/a\u003E.",
    "published": 1,
    "volume": 0.01
  },
  "systems": {
    "30000137": {
      "solarSystemID": 30000137,
      "solarSystemName": "Eskunen",
      "security": 0.6252939
    },
   ...
  },
  "stationNames": {
    "60001810": "Hirtamon VII - Moon 6 - Zainou Biotech Production",
    "60003346": "Otitoh VII - Moon 3 - Chief Executive Panel Academy",
    "60000919": "Ikami VI - Moon 13 - Caldari Provisions Food Packaging",
    "60015002": "Aokannitoh VII - Moon 2 - School of Applied Knowledge",
    ...
  },
  "structureNames": {
    "1043159223409": "Hentogaira - EDI-HQ",
    "1042508032148": "Perimeter - Tranquility Trading Tower",
    "1044752365771": "Perimeter - 0.0% Fence Tax Haven",
    ...
  },
  "orders": [
    {
      "duration": 90,
      "isBuyOrder": false,
      "issued": 1716186885000,
      "locationId": 60015027,
      "minVolume": 1,
      "orderId": 6789042859,
      "price": 25,
      "range": "REGION",
      "systemId": 30030141,
      "regionId": 10000002,
      "typeId": 34,
      "volumeRemain": 144247,
      "volumeTotal": 144247
    },
    ...
  ]
}
```

**itemType** содержит базовую информацию о товаре.

**systems** содержит информацию о системах. Наибольший интерес представляют следующие данные:
- solarSystemName - название системы;
- security - статус безопасности системы. При значении security >= 0.5 система считается безопасной,
при значении 0.5 > security > 0.0 система является небезопасной, при значении security <= 0.0 - опасной.

**stationNames** и **structureNames** содержат информация о станциях, где торгуется товар.

**orders** содержит информацию о заказах. Стоит отметить, что параметр isBuyOrder определяет тип заказа - 
покупка или продажа товара. Также ордер связан с остальными полями следующим образом:
- locationId содержит ID станции или структуры;
- systemId содержит ID системы.

**ПРИМЕЧАНИЕ**: ответ API содержит заголовок Expires - "время жизни" данных. Если сделать запрос на сервер до истечения
этого срока, новые данные получены не будут, а вернутся старые. Это стоит учитывать и хэшировать полученные данные.

## 4. План разработки

### Этап 1. Создание файла README.md и базовой структуры проекта.

### Этап 2. Создание тестовых команд /start и /help, а также структуры базы данных.

### Этап 3. Реализация команд /stats, /wtb, /wts. Хэширование данных.

### Этап 4. Реализации команды /history
