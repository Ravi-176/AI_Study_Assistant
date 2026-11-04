import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'dart:io';

class APIService{
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'http://192.168.29.133:8000',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds:10),
    ),
  );
  Future<Response<dynamic>> getProtectedData() async{
    final user = FirebaseAuth.instance.currentUser;
    if(user==null){
      throw Exception("Please login first!");
    }
    final idToken = await user.getIdToken();
   
    return  await _dio.get(
      '/auth/me',
      options: Options(
        headers: {
          'Authorization': 'Bearer $idToken',
        },
      ),
    );
  }
  Future<Response<dynamic>> getDocuments() async{
    final user = FirebaseAuth.instance.currentUser;
    
    if(user==null){
      throw Exception("Please login first");
    }
    final idToken = await user.getIdToken();
    
    return await _dio.get(
      "/documents",
      options: Options(
        headers:{
            'Authorization':'Bearer $idToken',
        }
      ),
    );

  }
  Future<Response<dynamic>> uploadDocument(File file) async{
    final user = FirebaseAuth.instance.currentUser;
    if(user==null){
      throw Exception("Please login first");
    }
    final idToken = await user.getIdToken();
  
    final formData = FormData.fromMap({
      'file':await MultipartFile.fromFile(
        file.path,
        filename: file.uri.pathSegments.last,
      )
    });
    return await _dio.post(
      '/documents/upload',
      data: formData,
      options: Options(
        headers:{
          'Authorization':'Bearer $idToken',
        },
      ),
    );
  }
}