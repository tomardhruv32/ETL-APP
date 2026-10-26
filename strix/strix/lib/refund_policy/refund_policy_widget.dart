import '/flutter_flow/ff_builtin_enums.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'refund_policy_model.dart';
export 'refund_policy_model.dart';

/// Generate a Good privacy policy page
class RefundPolicyWidget extends StatefulWidget {
  const RefundPolicyWidget({super.key});

  static String routeName = 'RefundPolicy';
  static String routePath = '/refundPolicy';

  @override
  State<RefundPolicyWidget> createState() => _RefundPolicyWidgetState();
}

class _RefundPolicyWidgetState extends State<RefundPolicyWidget> {
  late RefundPolicyModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RefundPolicyModel());

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).secondaryBackground,
                shape: BoxShape.rectangle,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding: EdgeInsets.all(24.0),
                    child: Container(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment:
                                (FFMainAxisAlignment.spaceBetween).flutterValue,
                            children: [
                              Text(
                                'Refund Policy',
                                style: FlutterFlowTheme.of(context)
                                    .headlineMedium
                                    .override(
                                      font: GoogleFonts.inter(
                                        fontWeight: FontWeight.bold,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .headlineMedium
                                            .fontStyle,
                                      ),
                                      color: FlutterFlowTheme.of(context)
                                          .primaryText,
                                      letterSpacing: 0.0,
                                      fontWeight: FontWeight.bold,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .headlineMedium
                                          .fontStyle,
                                      lineHeight: 1.4,
                                    ),
                              ),
                              InkWell(
                                splashColor: Colors.transparent,
                                focusColor: Colors.transparent,
                                hoverColor: Colors.transparent,
                                highlightColor: Colors.transparent,
                                onTap: () async {
                                  context.safePop();
                                },
                                child: Icon(
                                  Icons.close_sharp,
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                  size: 24.0,
                                ),
                              ),
                            ],
                          ),
                          Text(
                            'Last updated: October 22, 2026',
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
                        ].divide(SizedBox(height: 8.0)),
                      ),
                    ),
                  ),
                  Container(
                    height: 1.0,
                    decoration: BoxDecoration(
                      color: FlutterFlowTheme.of(context).alternate,
                      shape: BoxShape.rectangle,
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              flex: 1,
              child: Container(
                child: SingleChildScrollView(
                  primary: false,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Padding(
                        padding: EdgeInsets.all(24.0),
                        child: Container(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Expanded(
                                child: Container(
                                  decoration: BoxDecoration(
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryBackground,
                                    borderRadius: BorderRadius.circular(20.0),
                                  ),
                                  child: Padding(
                                    padding: EdgeInsetsDirectional.fromSTEB(
                                        10.0, 10.0, 10.0, 10.0),
                                    child: MarkdownBody(
                                      data:
                                          '''# Refund and Cancellation Policy\n\n**Effective Date:** October 22, 2026\n\n**Last Updated:** October 22, 2026\n\nThank you for choosing STRIX. We strive to provide a high-quality, AI-powered stock data analysis and screening experience. Please read this Refund and Cancellation Policy carefully before subscribing to any premium services, in-app purchases, or subscription plans. \n\nBy purchasing a subscription or accessing premium features on STRIX, you agree to the terms outlined below.\n\n### 1. General \"No Refund\" Policy for Digital Goods\n\nSTRIX provides digital analytical tools, software-as-a-service (SaaS), and immediate access to premium data filters. Because our products are completely digital and access is granted instantly upon purchase, **all sales are final and non-refundable**. \n\nWe do not offer refunds, partial refunds, or credits for:\n* Accidental purchases.\n* Unused time on a subscription.\n* Forgetting to cancel a trial or subscription before the renewal date.\n* Dissatisfaction with the user interface, available features, or app functionality after purchase.\n\n### 2. Subscription Cancellations\n\nYou are free to cancel your STRIX premium subscription at any time. \n\n* **How to Cancel:** You must cancel your subscription through the platform where you originally purchased it (e.g., your Google Play Store account, Apple App Store account, or the STRIX in-app billing portal).\n* **Post-Cancellation Access:** If you cancel your subscription, you will not receive a refund for the current billing cycle. However, you will continue to have full access to the premium features until the end of your current paid billing period.\n\n### 3. No Refunds for Market Performance (Trading Losses)\n\nAs stated in our Legal Disclaimer, STRIX is an analytical data screener, not an advisory service. \n* We **do not** guarantee any financial returns, profits, or specific market outcomes based on the use of our technical indexes, filters, or AI summaries.\n* **Under no circumstances** will a refund be issued because a user suffered trading/investment losses while using the data or features provided by STRIX. \n\n### 4. App Store and Payment Gateway Policies\n\nIf you purchase a STRIX subscription through a third-party marketplace (such as the Apple App Store or Google Play Store), your transaction is subject to the refund policies of that respective platform. \n* STRIX does not have the ability to process refunds or manage billing for purchases made through Apple or Google\'s native billing systems. You must contact Apple or Google customer support directly for any billing disputes.\n\n### 5. Exceptional Circumstances\n\nSTRIX reserves the right, at its sole discretion, to issue a refund or credit only under the following exceptional technical circumstances:\n* **Double Billing:** If a technical error on our end results in you being charged twice for the same billing cycle.\n* **Failure to Deliver:** If a major system outage prevents you from accessing your premium features for an extended, unreasonable period immediately following your purchase, and our support team cannot resolve the issue.\n\nTo report a billing error, you must contact us within **7 days** of the transaction date.\n\n### 6. Contact Us\n\nIf you believe you have experienced a billing error or have questions regarding this policy, please contact our support team:\n\n**Email:** contact.dhruv.tomar@gmail.com  \n**Address:** Agra\n\n*Please include your registered STRIX email address and a screenshot of your transaction receipt when contacting support.*''',
                                      selectable: true,
                                      onTapLink: (_, url, __) =>
                                          launchURL(url!),
                                    ),
                                  ),
                                ),
                              ),
                              Padding(
                                padding: EdgeInsetsDirectional.fromSTEB(
                                    0.0, 24.0, 0.0, 0.0),
                                child: Container(
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(24.0),
                                    shape: BoxShape.rectangle,
                                    border: Border.all(
                                      color: FlutterFlowTheme.of(context)
                                          .alternate,
                                      width: 1.0,
                                    ),
                                  ),
                                  child: Padding(
                                    padding: EdgeInsets.all(24.0),
                                    child: Container(
                                      child: Column(
                                        mainAxisSize: MainAxisSize.min,
                                        mainAxisAlignment:
                                            MainAxisAlignment.start,
                                        crossAxisAlignment:
                                            CrossAxisAlignment.center,
                                        children: [
                                          Text(
                                            'Have questions about your data?',
                                            style: FlutterFlowTheme.of(context)
                                                .bodyMedium
                                                .override(
                                                  font: GoogleFonts.inter(
                                                    fontWeight: FontWeight.w600,
                                                    fontStyle:
                                                        FlutterFlowTheme.of(
                                                                context)
                                                            .bodyMedium
                                                            .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme.of(
                                                          context)
                                                      .primaryText,
                                                  letterSpacing: 0.0,
                                                  fontWeight: FontWeight.w600,
                                                  fontStyle:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .bodyMedium
                                                          .fontStyle,
                                                  lineHeight: 1.4,
                                                ),
                                          ),
                                          Text(
                                            'Contact us at contact.dhruv.tomar@gmail.com',
                                            style: FlutterFlowTheme.of(context)
                                                .bodySmall
                                                .override(
                                                  font: GoogleFonts.inter(
                                                    fontWeight:
                                                        FlutterFlowTheme.of(
                                                                context)
                                                            .bodySmall
                                                            .fontWeight,
                                                    fontStyle:
                                                        FlutterFlowTheme.of(
                                                                context)
                                                            .bodySmall
                                                            .fontStyle,
                                                  ),
                                                  color: FlutterFlowTheme.of(
                                                          context)
                                                      .secondaryText,
                                                  letterSpacing: 0.0,
                                                  fontWeight:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .bodySmall
                                                          .fontWeight,
                                                  fontStyle:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .bodySmall
                                                          .fontStyle,
                                                  lineHeight: 1.4,
                                                ),
                                          ),
                                        ].divide(SizedBox(height: 16.0)),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              Container(
                                height: 24.0,
                              ),
                            ].divide(SizedBox(height: 24.0)),
                          ),
                        ),
                      ),
                    ],
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
