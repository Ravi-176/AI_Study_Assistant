import 'package:flutter/material.dart';
import 'package:mobile/screens/auth_screen.dart';
import 'package:mobile/screens/home_screen.dart';
import 'package:mobile/services/auth_service.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    final service = AuthService();
    return MaterialApp(
      title: 'AI Study Assistant',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
             colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.deepPurple
            ),
      ),
      home: StreamBuilder(
      stream:service.authStateChanges, 
      builder: (context,snapshot){
        if(snapshot.connectionState==ConnectionState.waiting){
          return const Scaffold(
            body:Center(
              child: CircularProgressIndicator(),
            ),
          );
        }
        if(snapshot.hasData){
          return const HomeScreen(
            title: 'AI Study Assistant'
            );
        }
        return const AuthScreen();
       },
      ),
    );
  }
}