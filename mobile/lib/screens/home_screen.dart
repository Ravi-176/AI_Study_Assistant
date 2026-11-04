import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:mobile/services/auth_service.dart';
import 'package:mobile/services/api_service.dart';




class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, required this.title}); 

  final String title;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  final AuthService _service = AuthService();
  final APIService _apiService = APIService();
  
  bool _isUploading=false;
  String _uploadMessage='';
  List<dynamic> _documents=[];
  bool _isLoadingDocs=false;
  String _docError = '';
  

  
  
  Future<void> _pickAndUploadPDF()async{ 
    
    try{
      final result = await FilePicker.pickFiles(
      type:FileType.custom,
      allowedExtensions: ["pdf"],
    );
    if(result.isEmpty){
      return;
    }
     final path = result.single.path;
    if(path==null){
      setState(() {
        _uploadMessage='Could not access the selected file.';
      });
      return;
    }
     //loading state
    setState(() {
      _isUploading=true;
      _uploadMessage='Uploading pdf...';
    });
    //data state
    final response=await _apiService.uploadDocument(File(path));
      if(!mounted){
        return;
      }
      setState(() {
        _uploadMessage="Upload successful\n"
                       "File:${response.data['file_name']??result.single.name}\n"
                       "Document id:${response.data['id']}";
      });
      await _loadDocuments();
    }
    catch (error){
      if(!mounted){
        return;
      }
      setState(() {
        _uploadMessage="Upload failed:$error";
      });
    }
    finally{
      if(mounted){
        setState(() {
          _isUploading=false;
        });
      }
    }
    
  }
  Future<void> _loadDocuments()async{
    //loading state
    setState(() {
      _isLoadingDocs=true;
      _docError='';
    });
    //data state
    try{
      final response = await _apiService.getDocuments();
       if(!mounted){
        return;
      }
      setState(() {
        _documents=response.data;
      });
    }
    catch(error){
      if(!mounted){
        return;
      }
      
      setState(() {
        _docError='Error loading documents:$error';
      });
    }
    finally{
      if(mounted){
        setState(() {
          _isLoadingDocs=false;
        });
      }
    }

  }
  @override
  void initState(){
    super.initState();
    _loadDocuments();
  }

  @override
  Widget build(BuildContext context) {
     
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions:[
          IconButton(onPressed: () async {
           await _service.signOut();
          }, 
          icon: const Icon(Icons.logout),
          tooltip: 'Log out',)
        ],
      ),
      body: ListView(
        padding:const EdgeInsets.all(16),
        children: [
          Text("Welcome to AI Study Assistant!",
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold
          ),
         ),
      
        const Divider(),
        ElevatedButton.icon(
        onPressed: _isUploading?null:_pickAndUploadPDF, 
        icon:const Icon(Icons.upload_file),
        label: Text(_isUploading?'Uploading file...':'Upload pdf'),
        ),
        if(_uploadMessage.isNotEmpty)
           Padding(padding: const EdgeInsets.all(12),
           child:Text(_uploadMessage),
          ),
        const Divider(height:32),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children:[
              Text('My Documents',
              style:TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            IconButton(
            onPressed: _isLoadingDocs?null:_loadDocuments, 
            icon:const Icon(Icons.refresh),
            tooltip: 'Refresh documents',
           ),
          ],
        ),
        if(_isLoadingDocs)
           const Center(
               child:CircularProgressIndicator(),
           )
        else if(_docError.isNotEmpty)
            Text(_docError)   
        else if(_documents.isEmpty)   
            Text('No documents uploaded yet!')
        else
            ..._documents.map((document){
                   return Card(
                    child: ListTile(
                      leading:const Icon(Icons.picture_as_pdf,
                          color: Colors.red,),
                      title:Text(document['file_name']),
                      subtitle: Text(
                        'Status: ${document['processing_status']}'
                      ),
                      trailing:const Icon(Icons.check_circle_outline) ,
                    ),
                   );
            },    


            ),    

       ],
      ),
      
     
    );
  }
}
