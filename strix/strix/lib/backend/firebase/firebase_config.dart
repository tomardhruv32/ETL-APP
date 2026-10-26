import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyDOtYQEuY5r6WF2OIxv-ZhNPkex0S-D4OI",
            authDomain: "rimuru-6h98cz.firebaseapp.com",
            projectId: "rimuru-6h98cz",
            storageBucket: "rimuru-6h98cz.firebasestorage.app",
            messagingSenderId: "142964889381",
            appId: "1:142964889381:web:c1d64406c554e9590feccc"));
  } else {
    await Firebase.initializeApp();
  }
}
