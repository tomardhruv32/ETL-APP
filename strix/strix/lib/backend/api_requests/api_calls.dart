import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';

import '/flutter_flow/flutter_flow_util.dart';
import 'api_manager.dart';

export 'api_manager.dart' show ApiCallResponse;

const _kPrivateApiFunctionName = 'ffPrivateApiCall';

class GeneralQueryCall {
  static Future<ApiCallResponse> call({
    String? userGeneralPrompt = '',
  }) async {
    final ffApiRequestBody = '''
{
  "user_prompt": ${userGeneralPrompt == null ? 'null' : '"${escapeStringForJson(userGeneralPrompt)}"'}
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'generalQuery',
      apiUrl: 'https://rimuru-hexa.onrender.com/query',
      callType: ApiCallType.POST,
      headers: {
        'Content-Type': 'application/json',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static String? generalAnswer(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.response''',
      ));
}

class StockQueryCall {
  static Future<ApiCallResponse> call({
    String? stockName = '',
    String? stockUserPrompt = '',
  }) async {
    final ffApiRequestBody = '''
{
  "user_prompt": ${stockUserPrompt == null ? 'null' : '"${escapeStringForJson(stockUserPrompt)}"'},
  "stock_name": ${stockName == null ? 'null' : '"${escapeStringForJson(stockName)}"'}
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'Stock query',
      apiUrl: 'https://rimuru-hexa.onrender.com/stock-query',
      callType: ApiCallType.POST,
      headers: {
        'Content-Type': 'application/json',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }
}

class ApiPagingParams {
  int nextPageNumber = 0;
  int numItems = 0;
  dynamic lastResponse;

  ApiPagingParams({
    required this.nextPageNumber,
    required this.numItems,
    required this.lastResponse,
  });

  @override
  String toString() =>
      'PagingParams(nextPageNumber: $nextPageNumber, numItems: $numItems, lastResponse: $lastResponse,)';
}

String _toEncodable(dynamic item) {
  return item;
}

String _serializeList(List? list) {
  list ??= <String>[];
  try {
    return json.encode(list, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("List serialization failed. Returning empty list.");
    }
    return '[]';
  }
}

String _serializeJson(dynamic jsonVar, [bool isList = false]) {
  jsonVar ??= (isList ? [] : {});
  try {
    return json.encode(jsonVar, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("Json serialization failed. Returning empty json.");
    }
    return isList ? '[]' : '{}';
  }
}

String? escapeStringForJson(String? input) {
  if (input == null) {
    return null;
  }
  final encoded = jsonEncode(input);
  return encoded.substring(1, encoded.length - 1);
}
