import '/backend/supabase/supabase.dart';
import '/components/filter_chip_widget.dart';
import '/components/observation_card3_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import '/index.dart';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'homepage_model.dart';
export 'homepage_model.dart';

/// **Master Design & Development Prompt: Strix Analytics Homepage (Figma &
/// FlutterFlow)**
///
/// **Context & Application Overview:**
/// Design and develop the Homepage for **Strix**, an educational and
/// data-driven Indian stock market application.
///
/// The app strictly adheres to SEBI compliance by acting solely as an
/// educational pattern-recognition tool, using terms like "Technical
/// Observations" and "Data Patterns" instead of "Signals" or "Buy/Sell." The
/// Homepage must be ultra-minimalist, highly aesthetic, and focus purely on
/// typography and static data presentation, as there are no live price
/// tickers or live charts.
///
/// **1. Figma UI/UX Design Instructions:**
///
/// * **Design System & Theme:** Use a clean, modern, dark or high-contrast
/// light theme. The aesthetic should feel premium and data-focused (think
/// Apple Stocks meets a clean FinTech dashboard).
/// * **Layout:** The core of the homepage is a full-screen or prominent
/// centered card interface. There is no traditional vertical scrolling feed.
/// * **The Swipeable Card Component:**
/// * Design a master "Data Card" that will act as the swipeable element.
/// * **Typography Hierarchy:**
/// * **Primary Text (H1/H2):** Stock Name (e.g., RELIANCE).
/// * **Secondary Text (Subtitle):** Date of Observation (e.g., 17 Oct 2026).
///
///
/// * **Visual Indicators (Badges/Chips):** Create a distinct, aesthetically
/// pleasing pill/chip component to display the "Observed Pattern." Assign
/// subtle, distinct color codes for the five categories: *Breakout, Momentum,
/// Strong Pullback, Volume Breakout, Strong Bullish*.
/// * **Empty State:** Design a beautiful "You're all caught up" card for when
/// the user finishes swiping through the day's data.
///
///
///
/// **2. FlutterFlow Implementation Instructions (Strictly Free Features):**
///
/// * **Widget Selection:** To achieve the swipeable card effect without
/// custom code or paid features, utilize the built-in **SwipeableStack**
/// widget. The SwipeableStack lets users browse a stack of cards by swiping
/// the top card away. It can be found under Layout Elements in the Widget
/// Palette.
/// * **Alternative Widget:** If a horizontal slider is preferred over a
/// stack, use the **PageView** widget configured with a horizontal scroll
/// direction and enabled page snapping. The PageView widget is used to create
/// swipeable pages horizontally or vertically.
/// * **Backend Query Integration:**
/// * Select the SwipeableStack widget and open the Backend Query in the
/// Properties Panel.
/// * Bind it to the database collection (containing the ~1000 rows of static
/// technical observations).
/// * Design a single SwipeableStack Page as the repeated card template. Bind
/// the Text widgets and pattern badges on that template page to the fields
/// from the current document or row. FlutterFlow will automatically generate
/// and display a card for each record returned by the query.
///
///
/// * **Swipe Customization:**
/// * In the SwipeableStack Properties, configure the "Card Display Count" to
/// show multiple stacked cards behind the top one for depth.
/// * Adjust the "Next Card Scale" (e.g., 0.9) to make the cards behind the
/// top card appear slightly smaller, creating a 3D stacking effect.
/// * Set the "Allowed Swipe Direction" to limit swipes to Horizontal (left
/// and right) if desired.
///
///
/// * **Interactive Swipe Buttons (Optional but recommended):**
/// * Place UI buttons (e.g., "Skip" and "Save/Bookmark") outside the
/// SwipeableStack so they remain visible as cards change.
/// * Add an "On Tap" action to these buttons, choose the "Swipeable Stack"
/// action, and select "Trigger Left Swipe" or "Trigger Right Swipe".
class HomepageWidget extends StatefulWidget {
  const HomepageWidget({super.key});

  static String routeName = 'Homepage';
  static String routePath = '/homepage';

  @override
  State<HomepageWidget> createState() => _HomepageWidgetState();
}

class _HomepageWidgetState extends State<HomepageWidget> {
  late HomepageModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HomepageModel());

    // On page load action.
    SchedulerBinding.instance.addPostFrameCallback((_) async {
      _model.momentumActiveFilter = false;
      _model.brakoutActiveFilter = true;
      _model.strongpullbackActiveFilter = false;
      _model.pullbackActiveFilter = false;
      _model.strongbullishActiveFilter = false;
      _model.strongvolumebreakoutActiveFilter = false;
      _model.volumebreakoutActiveFilter = false;
      safeSetState(() {});
    });

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    context.watch<FFAppState>();

    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        appBar: PreferredSize(
          preferredSize: Size.fromHeight(110.0),
          child: AppBar(
            backgroundColor: FlutterFlowTheme.of(context).secondaryBackground,
            automaticallyImplyLeading: false,
            title: Column(
              mainAxisSize: MainAxisSize.max,
              children: [
                Padding(
                  padding: EdgeInsetsDirectional.fromSTEB(0.0, 25.0, 0.0, 0.0),
                  child: Text(
                    'STRIX',
                    style: FlutterFlowTheme.of(context).bodyMedium.override(
                          font: GoogleFonts.roboto(
                            fontWeight: FontWeight.bold,
                            fontStyle: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .fontStyle,
                          ),
                          color: Color(0xFF1A365D),
                          fontSize: 40.0,
                          letterSpacing: 0.0,
                          fontWeight: FontWeight.bold,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                        ),
                  ),
                ),
                Padding(
                  padding: EdgeInsetsDirectional.fromSTEB(0.0, 5.0, 0.0, 10.0),
                  child: Text(
                    'AI Powered Stock Data Analysis',
                    style: FlutterFlowTheme.of(context).bodyMedium.override(
                          font: GoogleFonts.inter(
                            fontWeight: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .fontWeight,
                            fontStyle: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .fontStyle,
                          ),
                          letterSpacing: 0.0,
                          fontWeight: FlutterFlowTheme.of(context)
                              .bodyMedium
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                        ),
                  ),
                ),
              ],
            ),
            actions: [
              FlutterFlowIconButton(
                borderRadius: 8.0,
                buttonSize: 66.0,
                fillColor: Colors.transparent,
                icon: FaIcon(
                  FaIconData(const IconData(/* solidUserCircle */ 0xf2bd,
                      fontFamily: 'FontAwesomeSolid',
                      fontPackage: 'font_awesome_flutter')),
                  color: FlutterFlowTheme.of(context).secondaryText,
                  size: 40.0,
                ),
                onPressed: () async {
                  context.pushNamed(ProfilePageWidget.routeName);
                },
              ),
            ],
            centerTitle: true,
            toolbarHeight: 100.0,
            elevation: 1.0,
          ),
        ),
        body: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              height: 70.0,
              decoration: BoxDecoration(),
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0.0, 16.0, 0.0, 16.0),
                child: Container(
                  child: Container(
                    height: 28.0,
                    alignment: AlignmentDirectional(0.0, 0.0),
                    child: SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Padding(
                            padding: EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 0.0),
                            child: Container(
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                mainAxisAlignment: MainAxisAlignment.start,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied = 'BREAKOUT';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = true;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel1,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active: _model.brakoutActiveFilter,
                                        label: 'Filter (Breakout)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied = 'MOMENTUM';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = true;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel2,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active: _model.momentumActiveFilter,
                                        label: 'Filter (Momentum)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied =
                                          'STRONG BULLISH';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = true;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel3,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active:
                                            _model.strongbullishActiveFilter,
                                        label: 'Filter (Strong Bullish)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied =
                                          'VOLUME BREAKOUT';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = true;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel4,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active:
                                            _model.volumebreakoutActiveFilter,
                                        label: 'Filter (Volume Breakout)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied = 'PULLBACK';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = true;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel5,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active: _model.pullbackActiveFilter,
                                        label: 'Filter (PULLBACK)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied =
                                          'STRONG PULLBACK';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = true;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          false;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel6,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active:
                                            _model.strongpullbackActiveFilter,
                                        label: 'Filter (STRONG PULLBACK)',
                                      ),
                                    ),
                                  ),
                                  InkWell(
                                    splashColor: Colors.transparent,
                                    focusColor: Colors.transparent,
                                    hoverColor: Colors.transparent,
                                    highlightColor: Colors.transparent,
                                    onTap: () async {
                                      FFAppState().filterApplied =
                                          'STRONG VOLUME BREAKOUT';
                                      safeSetState(() {});
                                      _model.momentumActiveFilter = false;
                                      _model.brakoutActiveFilter = false;
                                      _model.strongpullbackActiveFilter = false;
                                      _model.pullbackActiveFilter = false;
                                      _model.strongbullishActiveFilter = false;
                                      _model.strongvolumebreakoutActiveFilter =
                                          true;
                                      _model.volumebreakoutActiveFilter = false;
                                      safeSetState(() {});
                                    },
                                    child: wrapWithModel(
                                      model: _model.filterChipModel7,
                                      updateCallback: () => safeSetState(() {}),
                                      child: FilterChipWidget(
                                        active: _model
                                            .strongvolumebreakoutActiveFilter,
                                        label:
                                            'Filter (STRONG VOLUME BREAKOUT)',
                                      ),
                                    ),
                                  ),
                                ].divide(SizedBox(width: 16.0)),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              flex: 1,
              child: Stack(
                alignment: AlignmentDirectional(0.0, 0.0),
                children: [
                  Opacity(
                    opacity: 0.5,
                    child: Transform.rotate(
                      angle: 2.0 * (math.pi / 180),
                      alignment: AlignmentDirectional(0.0, 0.0),
                      child: Container(
                        width: 320.0,
                        height: 440.0,
                        decoration: BoxDecoration(
                          color:
                              FlutterFlowTheme.of(context).secondaryBackground,
                          borderRadius: BorderRadius.circular(24.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: FlutterFlowTheme.of(context).alternate,
                            width: 1.0,
                          ),
                        ),
                      ),
                    ),
                  ),
                  FutureBuilder<List<OpportunitiesRow>>(
                    future: OpportunitiesTable().queryRows(
                      queryFn: (q) => q
                          .like(
                            'signal',
                            FFAppState().filterApplied,
                          )
                          .order('created_at'),
                      limit: 600,
                    ),
                    builder: (context, snapshot) {
                      // Customize what your widget looks like when it's loading.
                      if (!snapshot.hasData) {
                        return Center(
                          child: SizedBox(
                            width: 50.0,
                            height: 50.0,
                            child: CircularProgressIndicator(
                              valueColor: AlwaysStoppedAnimation<Color>(
                                FlutterFlowTheme.of(context).primary,
                              ),
                            ),
                          ),
                        );
                      }
                      List<OpportunitiesRow> listViewOpportunitiesRowList =
                          snapshot.data!;

                      return ListView.builder(
                        padding: EdgeInsets.zero,
                        shrinkWrap: true,
                        scrollDirection: Axis.vertical,
                        itemCount: listViewOpportunitiesRowList.length,
                        itemBuilder: (context, listViewIndex) {
                          final listViewOpportunitiesRow =
                              listViewOpportunitiesRowList[listViewIndex];
                          return ObservationCard3Widget(
                            key: Key(
                                'Key3l3_${listViewIndex}_of_${listViewOpportunitiesRowList.length}'),
                            symbol: listViewOpportunitiesRow.stockName,
                            date: dateTimeFormat(
                                "yMMMd", listViewOpportunitiesRow.signalDate),
                            pattern: listViewOpportunitiesRow.signalScore
                                ?.toString(),
                            description: () {
                              if (listViewOpportunitiesRow.signal ==
                                  'PULLBACK') {
                                return 'A pullback is a short-term, temporary decline in the price of an asset within an ongoing, broader upward trend, often reflecting a brief pause in market activity.';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'STRONG VOLUME BREAKOUT') {
                                return 'This occurs when an asset\'s price moves beyond an established historical resistance or support level, accompanied by trading volume that is significantly higher than the historical average';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'VOLUME BREAKOUT') {
                                return 'A volume breakout is characterized by a price movement past a specific technical level that coincides with a noticeable increase in trading volume compared to recent standard activity.';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'STRONG BULLISH') {
                                return 'This term describes a historically observed market pattern where sustained upward price momentum indicates aggressive buying interest, reflecting an overall optimistic technical data profile for the asset.';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'STRONG PULLBACK') {
                                return 'A strong pullback represents a relatively deep and rapid retracement in an asset\'s price against the prevailing primary trend, highlighting a sharp but potentially temporary shift in market momentum.';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'BREAKOUT') {
                                return 'A breakout happens when historical data shows an asset\'s price advancing above a defined resistance level or dropping below a support level, suggesting a potential new price channel.';
                              } else if (listViewOpportunitiesRow.signal ==
                                  'MOMENTUM') {
                                return 'Momentum measures the velocity and magnitude of a price trend over a specific period, providing objective data on the accelerating or decelerating strength of recent market movements.';
                              } else {
                                return 'Data is loading....';
                              }
                            }(),
                            signal: listViewOpportunitiesRow.signal,
                          );
                        },
                      );
                    },
                  ),
                ],
              ),
            ),
            Container(
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).primaryBackground,
                shape: BoxShape.rectangle,
              ),
              child: Padding(
                padding: EdgeInsets.all(32.0),
                child: Container(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Container(
                        height: 50.0,
                        decoration: BoxDecoration(
                          color: FlutterFlowTheme.of(context).primary,
                          borderRadius: BorderRadius.circular(100.0),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.arrow_upward,
                              color: FlutterFlowTheme.of(context)
                                  .secondaryBackground,
                              size: 24.0,
                            ),
                            Text(
                              'Scoll up and down to navigate',
                              textAlign: TextAlign.justify,
                              style: FlutterFlowTheme.of(context)
                                  .bodyMedium
                                  .override(
                                    font: GoogleFonts.inter(
                                      fontWeight: FontWeight.bold,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .bodyMedium
                                          .fontStyle,
                                    ),
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryBackground,
                                    letterSpacing: 0.0,
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontStyle,
                                  ),
                            ),
                            Icon(
                              Icons.arrow_downward,
                              color: FlutterFlowTheme.of(context)
                                  .secondaryBackground,
                              size: 24.0,
                            ),
                          ].divide(SizedBox(width: 32.0)),
                        ),
                      ),
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.info_outlined,
                            color: FlutterFlowTheme.of(context).secondaryText,
                            size: 12.0,
                          ),
                          Text(
                            'Data Patterns for Analysis · Not Investment Advice',
                            style: FlutterFlowTheme.of(context)
                                .labelSmall
                                .override(
                                  font: GoogleFonts.inter(
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .labelSmall
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelSmall
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context)
                                      .secondaryText,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .labelSmall
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .labelSmall
                                      .fontStyle,
                                  lineHeight: 1.4,
                                ),
                          ),
                        ].divide(SizedBox(width: 4.0)),
                      ),
                    ].divide(SizedBox(height: 24.0)),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
