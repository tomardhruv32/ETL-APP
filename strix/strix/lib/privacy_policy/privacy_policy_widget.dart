import '/flutter_flow/ff_builtin_enums.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'privacy_policy_model.dart';
export 'privacy_policy_model.dart';

/// Generate a Good privacy policy page
class PrivacyPolicyWidget extends StatefulWidget {
  const PrivacyPolicyWidget({super.key});

  static String routeName = 'PrivacyPolicy';
  static String routePath = '/privacyPolicy';

  @override
  State<PrivacyPolicyWidget> createState() => _PrivacyPolicyWidgetState();
}

class _PrivacyPolicyWidgetState extends State<PrivacyPolicyWidget> {
  late PrivacyPolicyModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => PrivacyPolicyModel());

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
                                'Privacy Policy',
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
                                          '''# Privacy Policy for STRIX\n\n**Effective Date:** October 20, 2026  \n**Last Updated:** October 20, 2026  \n\nWelcome to STRIX (\"we,\" \"our,\" or \"us\"). STRIX is an AI-powered stock data analysis and screening tool. We are committed to protecting your privacy and ensuring that your personal data is handled securely and responsibly in accordance with the **Digital Personal Data Protection Act, 2023 (DPDPA)**, the **Information Technology Act, 2000**, and applicable regulatory frameworks in India.\n\nThis Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our mobile application and related services (collectively, the \"Service\").\n\n---\n\n## 1. Information We Collect\n\nTo provide our purely analytical screening services, we collect the minimum necessary data:\n\n### A. Information You Provide to Us\n*   **Authentication Data:** When you log in using third-party single sign-on (e.g., \"Sign in with Google\"), we receive your name, email address, profile picture URL, and a unique authentication token.\n\n### B. Information Collected Automatically\n*   **Usage Data:** We collect data on how you interact with the app, such as the filters you use (e.g., Breakout, Momentum), stocks viewed, search history within the app, and timestamped interactions.\n*   **Device & Technical Data:** IP address, device type, operating system version, app version, and crash diagnostic data to ensure app stability.\n\n### C. What We Do NOT Collect\n*   **Financial Data:** We **do not** collect, request, or store your bank account numbers, UPI PINs, credit/debit card details, demat account credentials, or broker API trading tokens. STRIX is read-only and does not execute trades.\n\n---\n\n## 2. How We Use Your Information\n\nWe process your data strictly for the following purposes:\n*   **Authentication & Security:** To create and maintain your user session and secure your profile.\n*   **App Functionality:** To save your user preferences, filter settings, and display the relevant mathematical and technical index data for your chosen stocks.\n*   **Service Improvement:** To analyze crash reports and aggregated usage metrics to improve our AI processing and user interface.\n*   **Legal Compliance:** To comply with statutory data logging requirements under Indian law.\n\n---\n\n## 3. Data Processing and AI Analytics Disclaimer\n\n*   **Public Data Processing:** Our AI engines and mathematical models process public exchange market data. Your personal account data is not fed into public Large Language Models (LLMs) or used to train external algorithms without explicit, anonymized consent.\n*   **No Investment Advice:** Usage data is used to improve our *software*, not to tailor financial advice. STRIX provides objective mathematical screening (e.g., \"Technical Index,\" \"Volume Surge\") and is **not a SEBI-registered Investment Adviser or Research Analyst**. \n\n---\n\n## 4. How We Share Your Information\n\nWe do not sell, rent, or trade your personal data. We may share your data only in the following limited circumstances:\n*   **Service Providers:** With trusted cloud hosting providers, database managers, and authentication services (like Google) who operate under strict confidentiality agreements to facilitate our Service.\n*   **Legal and Regulatory Authorities:** If mandated by law, court order, or requested by statutory authorities (such as SEBI, CERT-In, or law enforcement agencies) to comply with legal obligations in India.\n\n---\n\n## 5. Data Security and Retention\n\n*   **Security:** We implement industry-standard encryption (TLS/SSL) for data in transit and secure server architectures for data at rest to protect against unauthorized access, alteration, or destruction.\n*   **Retention:** We retain your account data for as long as your account is active. If you delete your account, we will purge your personal identifiers, retaining only anonymized telemetry data or logs legally required under the IT Act guidelines.\n\n---\n\n## 6. Your Rights (DPDPA 2023)\n\nAs a user in India, you hold the following rights regarding your personal data:\n*   **Right to Access:** You can request a summary of the personal data we hold about you.\n*   **Right to Correction:** You can update or correct inaccuracies in your profile information.\n*   **Right to Erasure:** You can request the deletion of your account and associated personal data at any time via the app settings.\n*   **Right to Withdraw Consent:** You can disconnect your Google account or withdraw consent for data processing, which may result in the termination of app services.\n*   **Right to Nominate:** You may nominate another individual to exercise your rights in the event of death or incapacity.\n\n---\n\n## 7. Third-Party Links\n\nThe STRIX app may contain links to third-party websites or API integrations. We are not responsible for the privacy practices or content of these external entities. We encourage you to read their privacy policies.\n\n---\n\n## 8. Updates to This Privacy Policy\n\nWe may update this policy periodically to reflect changes in our app features or regulatory updates. Any material changes will be communicated via an in-app notification. The \"Last Updated\" date at the top will reflect the current version.\n\n---\n\n## 9. Contact Us & Grievance Officer\n\nIn accordance with the Information Technology Act, 2000 and DPDPA, 2023, if you have any questions, concerns, or grievances regarding this Privacy Policy or your data, please contact our Grievance Officer:\n\n**Name:**Dhruv Tomar  \n**Designation:** Developer\n**Email:** contact.dhruv.tomar@gmail.com  \n**Address:** Agra\n\n*We will acknowledge your grievance within 72 hours and resolve it within 30 days of receipt.*''',
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
