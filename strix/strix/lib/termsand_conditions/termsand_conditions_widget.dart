import '/flutter_flow/ff_builtin_enums.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'termsand_conditions_model.dart';
export 'termsand_conditions_model.dart';

/// Generate a Good privacy policy page
class TermsandConditionsWidget extends StatefulWidget {
  const TermsandConditionsWidget({super.key});

  static String routeName = 'TermsandConditions';
  static String routePath = '/termsandConditions';

  @override
  State<TermsandConditionsWidget> createState() =>
      _TermsandConditionsWidgetState();
}

class _TermsandConditionsWidgetState extends State<TermsandConditionsWidget> {
  late TermsandConditionsModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => TermsandConditionsModel());

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
                                'Terms & Conditions',
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
                                          '''# Terms and Conditions\n\n**Effective Date:** October 22, 2026\n**Last Updated:** October 22, 2026\n\nWelcome to STRIX (\"we,\" \"our,\" or \"us\"). These Terms and Conditions (\"Terms\") govern your access to and use of the STRIX mobile application, website, and related services (collectively, the \"Service\"). \n\nBy downloading, accessing, or using STRIX, you agree to be bound by these Terms. If you do not agree with any part of these Terms, you must not use our Service.\n\n### 1. Eligibility\nYou must be at least 18 years old and capable of forming a binding contract under applicable law (including the Indian Contract Act, 1872) to use STRIX. By using the Service, you represent and warrant that you meet these eligibility requirements.\n\n### 2. Nature of the Service (Not Financial Advice)\nSTRIX provides automated, AI-powered stock market data analysis, mathematical screeners, and technical indicators based on publicly available exchange data. \n* **No Advisory Relationship:** We are not registered with SEBI as an Investment Adviser (IA) or Research Analyst (RA). \n* **No Recommendations:** The data, filters (e.g., Breakout, Momentum), and indices provided are for informational and educational purposes only. They do not constitute financial, investment, legal, or tax advice.\n* You are solely responsible for your own investment decisions and the evaluation of any data provided by the App. \n\n### 3. User Accounts and Security\nTo access certain features, you may be required to register using a third-party authentication provider (e.g., Google Sign-In).\n* You are responsible for maintaining the confidentiality of your account credentials.\n* You agree to notify us immediately of any unauthorized use of your account.\n* We reserve the right to suspend or terminate your account if any information provided is found to be false, misleading, or in violation of these Terms.\n\n### 4. Prohibited Conduct\nWhen using STRIX, you agree **not** to:\n* Use the Service for any illegal purpose or in violation of any local, state, national, or international law (including SEBI regulations).\n* Copy, reproduce, distribute, or create derivative works of our algorithms, UI designs, or AI insights without our explicit written permission.\n* Use automated scripts, spiders, or scrapers to extract data from STRIX.\n* Resell, redistribute, or use STRIX data to provide commercial advisory services to third parties.\n* Attempt to reverse-engineer, decompile, or hack the STRIX application or servers.\n\n### 5. Intellectual Property\nAll content, features, algorithms, logos, UI designs, and underlying code within STRIX are the exclusive property of STRIX and its licensors, protected by Indian and international copyright, trademark, and intellectual property laws. Your use of the App does not grant you any ownership rights.\n\n### 6. Subscriptions and Payments\nIf STRIX introduces premium paid features:\n* Payments will be processed through third-party platforms (e.g., Google Play Store, Apple App Store, or authorized payment gateways).\n* All purchases are subject to our **Refund and Cancellation Policy**. \n* We reserve the right to change our pricing or subscription models at any time, with reasonable prior notice to active subscribers.\n\n### 7. Disclaimer of Warranties\nThe Service is provided on an \"AS IS\" and \"AS AVAILABLE\" basis. \n* We make no warranties, expressed or implied, regarding the accuracy, reliability, or completeness of the market data or AI calculations provided.\n* We do not warrant that the App will be uninterrupted, error-free, or completely secure from cyber threats.\n\n### 8. Limitation of Liability\nTo the maximum extent permitted by applicable law, STRIX, its founders, and affiliates shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages, including but not limited to:\n* Financial or trading losses incurred by relying on STRIX data.\n* Loss of profits, data, or goodwill.\n* Service interruptions or system failures.\nIn no event shall our total aggregate liability to you exceed the total amount paid by you to STRIX (if any) in the past six (6) months.\n\n### 9. Indemnification\nYou agree to indemnify and hold harmless STRIX, its affiliates, and employees from any claims, damages, obligations, losses, liabilities, costs, or debts arising from:\n* Your use of and access to the Service.\n* Your violation of any term of these Terms and Conditions.\n* Your violation of any third-party right or statutory regulation.\n\n### 10. Third-Party Links\nSTRIX may contain links to third-party websites or services that are not owned or controlled by us. We assume no responsibility for the content, privacy policies, or practices of any third-party sites.\n\n### 11. Termination\nWe may terminate or suspend your access to STRIX immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach these Terms. Upon termination, your right to use the Service will cease immediately.\n\n### 12. Governing Law and Jurisdiction\nThese Terms shall be governed and construed in accordance with the laws of India. Any dispute arising out of or in connection with these Terms shall be subject to the exclusive jurisdiction of the courts located in [Insert Your City/State, e.g., New Delhi, India].\n\n### 13. Changes to Terms\nWe reserve the right to modify or replace these Terms at any time. If a revision is material, we will provide at least 15 days\' notice prior to any new terms taking effect. By continuing to access or use our Service after those revisions become effective, you agree to be bound by the revised terms.\n\n### 14. Contact Information\nIf you have any questions about these Terms, please contact us:\n* **Email:** contact.dhruv.tomar@gmail.com\n* **Address:** Agra''',
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
