
# http://www.delivery-auto.com.ua/userfs/LocalizableFiles/ru-RU/delivery-api/695d84a6-1de3-40ba-9634-da3cb97c7471_API%20%D0%BF%D0%BE%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B5%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D0%BE%D0%B2%20%D1%81%20Delivery%20v3%202%20(%D0%9E%D1%84%D0%BE%D1%80%D0%BC%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5).pdf


# https://www.delivery-auto.com.ua/ru-RU/Home/Api#buttons_a


'''

var apiKey = 'CDBFE2D5-BF02-4C0D-B7D6-5CF277761C50';
var apiSecretKey = '6c131f01b99dfac3529d0cd68b1d6649';

var getHMAC = function (key, timestamp) {
    var hash = CryptoJS.HmacSHA1(key + timestamp, apiSecretKey);
    return hash.toString();
};

var data = {
    "culture": "ru-RU",
    "flSave": "false",
    "debugMode": "true",
    "receiptsList": [
        {
            "senderid": "CDBFE2D5-BF02-4C0D-B7D6-5CF277761C50",
            "areasSendId": "4577d856-322b-e311-8b0d-00155d037960",
            "areasResiveId": "16617df3-a42a-e311-8b0d-00155d037960",
            "warehouseSendId": "5f2af375-5d70-e211-9ce1-00155d012a15",
            "warehouseResiveId": "bdff546c-cb16-e211-89ed-00155d053b5d",
            "dateSend": "2018-02-20T00:00:00",
            "deliveryScheme": 0,
            "posibleResiverReceipt_1": "ee5df311-6565-44d5-84f6-14875aa3e208",
            "posibleResiverReceipt_2": "",
            "posibleResiverReceipt_3": "",
            "posibleResiverReceipt_4": "",
            "currency": 100000000,
            "InsuranceValue": 5000,
            "payerInsuranceId": "1aa70d22-1209-e511-b3b5-000d3a200160",
            "payerType": 1,
            "paymentType": 0,
            "paymentTypeInsuranse": 0,
            "deliveryAddressId": "",
            "deliveryContactName": "",
            "deliveryContactPhone": "",
            "DeliveryComment": "",
            "ReturnDocuments": false,
            "climbingToFloor": 0,
            "CustomsCost": 0,
            "CustomsCurrency": 100000000,
            "CustomsDocuments": false,
            "CustomsDescriptions": "",
            "cashOnDeliveryType": 2,
            "CashOnDeliveryValuta": 100000000,
            "CashOnDeliveryValue": 5000,
            "CashOnDeliveryCardId": "",
            "CashOnDeliveryWarehouseId": "5f2af375-5d70-e211-9ce1-00155d012a15",
            "CashOnDeliverySenderFullName": "Семёнов Семён Семёнович",
            "CashOnDeliverySenderPhone": "0958888888",
            "CashOnDeliveryRasschSchetId": "",
            "CashOnDeliveryReceiverFullName": "Петров Пётр Петрович",
            "CashOnDeliveryReceiverPhone": "0671234567",
            "parentNumber": "",
            "CashOnDeliveryDescription": "Описание",
            "CashOnDeliveryPayerAccountId": "ee5df311-6565-44d5-84f6-14875aa3e208",
            "pickUpDate": "",
            "pickUpContactName": "",
            "pickUpContactPhone": "",
            "pickUpAddressId": "",
            "descentFromFloor": 0,
            "category": [
                {
                    "categoryId": "00000000-0000-0000-0000-000000000000",
                    "cargoCategoryId": "f506d03b-9e36-e311-8b0d-00155d037960",
                    "countPlace": 1,
                    "helf": 1,
                    "size": 0.3,
                    "isEconom": false,
                    "PartnerNumber": "\"\""
                }
            ]
        }
    ]
};

$.ajax({
    url: 'https://www.delivery-auto.com/api/v4/Public/PostCreateReceipts',
    type: "POST",
    data: data,
    dataType: 'json',
    beforeSend: function (request) {
        request.setRequestHeader('HMACAuthorization', 'amx ' + apiKey + ':' + timestamp + ':' + getHMAC(apiKey, timestamp));
    },
    success: function (data) {
        debugger;
        if (data.status == true) {
            debugger;
        }
    },
    error: alert('error');
});


'''