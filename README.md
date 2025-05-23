В ходе работы над проектом мною было выделено три принципиально различных пользователя данного продукта:
  1.	User (U или MU) – основной пользователь, человек сдающий в фандомат возвратную тару. После сдачи бутылки отправляет код с дисплея на фандомате телеграм-боту
  2.	Bottle vending machine или Reverse vending machine (RVM) – фандомат, принимающий возвратную тару. После сдачи человеком бутылки, отправляет post запрос на сервер с количеством начисленных баллов. В ответ получает код, который необходимо вывести на дисплей
  3.	Partner Company Server (PCS) – сервер компании-партнера, которая обменивает бонусы на свои услуги. PCS выполняет get запрос на сервер с номером карты (которую MU может узнать через телеграм-бота и ввести на сайте) и получает в ответ баланс карты. Также PCS выполняет post запрос на сервер с номером карты и количеством списываемых баллов. MU подтверждает данную операцию через телеграм-бота, и с его счета списывается это количество баллов. PCS получает в ответ либо код ошибки (несуществующая карта, отклонение операции, недостаточно баллов для списания), либо подтверждение удавшейся операции.

Далее было решено разделить создание проекта на две части: написание телеграм-бота и написание сервера (RESTful API). Для их слияния было решено использовать Git.
Написание Telegram-бота
При создании телеграм-бота было выделено несколько основных функций, на которые должен уметь отвечать телеграм-бот:
  1.	start – базовая команда, вызывается автоматически при открытии телеграм-бота. Программа вносит в DB_Person TELEGRAM_ID (ID, который присваивается каждому пользователю телеграмма), CARD_ID (номер карт, которую генерирует сама программа), BALANCE (принимается по умолчанию равным 0). Также присылает пользователю приветственное сообщение и сообщение, присылаемое функцией help.
  2.	help – вспомогательная команда, которая присылает пользователю сообщение с описанием функционала телеграм-бота.
  3.	info – вспомогательная программ, присылает пользователю сообщения с текстом описания того, как можно потратить бонусные баллы.
  4.	get_card – основная команда, присылает пользователю сообщение, в котором содержится номер карты пользователя
  5.	balance – вспомогательная команда, присылает пользователю сообщение с количеством баллов на его карте
  6.	topup – основная команда, присылает пользователю сообщение с просьбой ввести код с дисплея RVM. После введения пользователем кода, программа либо сообщает о несуществовании данного кода, либо начисляет баллы и присылает сообщение с балансом карты, одновременно удаляя код из DB_Codes.

Кроме этого, была прописана отдельная функция для согласования (посредством телеграм-бота) с MU списания баллов.
Написание сервера (RESTful API) 
Написание сервера также было разбито на отдельные подзадачи:
  1.	API для обработки post запроса от RVM, осуществляется по ссылке /machine/write/points, в json-формате, с обязательным полем “points”. Сервер, получив данный запрос, сформирует код, внесет его в DB_Codes и ответит на запрос, создав ответ в json-формате с обязательным полем “display_code” и HTTP-кодом ответа 201.
  2.	API для обработки get запроса от PCS, осуществляется по ссылке /machine/read/balance, в json-формате, с обязательным полем “card_id”. Сервер, получив данный запрос, проверит наличие карты с таким номером в DB_Person и ответит на запрос, создав ответ в json-формате с обязательным полем “balance” и HTTP-кодом ответа 201 или с обязательным полем “error” и HTTP-кодом ответа 405.
  3.	API для обработки post запроса от PCS, осуществляется по ссылке /machine/change/balance, в json-формате, с обязательными полями “card_id” и “summ”. Сервер, получив данный запрос, проверит наличие карты с таким номером в DB_Person, проверит баланс карты на наличие хотя бы <summ> баллов, согласует списание баллов с MU (посредством телеграм-бота) и ответит на запрос, создав ответ в json-формате с HTTP-кодом ответа 201 или с обязательным полем “error” и HTTP-кодом ответа 405.
В поле “error” находится одна из ошибок: “CardError”, “LowBalanceError”, “AgreementError”.
