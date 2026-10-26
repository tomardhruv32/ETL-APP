import '../database.dart';

class OpportunitiesTable extends SupabaseTable<OpportunitiesRow> {
  @override
  String get tableName => 'opportunities';

  @override
  OpportunitiesRow createRow(Map<String, dynamic> data) =>
      OpportunitiesRow(data);
}

class OpportunitiesRow extends SupabaseDataRow {
  OpportunitiesRow(Map<String, dynamic> data) : super(data);

  @override
  SupabaseTable get table => OpportunitiesTable();

  DateTime? get createdAt => getField<DateTime>('created_at');
  set createdAt(DateTime? value) => setField<DateTime>('created_at', value);

  String get instrumentKey => getField<String>('instrument_key')!;
  set instrumentKey(String value) => setField<String>('instrument_key', value);

  String? get stockName => getField<String>('stock_name');
  set stockName(String? value) => setField<String>('stock_name', value);

  String? get signal => getField<String>('signal');
  set signal(String? value) => setField<String>('signal', value);

  double? get signalScore => getField<double>('signal_score');
  set signalScore(double? value) => setField<double>('signal_score', value);

  DateTime? get signalDate => getField<DateTime>('signal_date');
  set signalDate(DateTime? value) => setField<DateTime>('signal_date', value);
}
