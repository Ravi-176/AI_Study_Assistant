import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:mobile/services/auth_service.dart';

class AuthScreen extends StatefulWidget{
  const AuthScreen({super.key});
  @override
  State<AuthScreen> createState() => _AuthScreenState();
}
class _AuthScreenState extends State<AuthScreen>{
  final AuthService _service = AuthService();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isSignedUp = true;
  bool _isLoading = false;
  Future<void> _submit() async{
    setState(() {
      _isLoading = true;
    });
    try{
      if(_isSignedUp){
      await _service.signIn(_emailController.text,
       _passwordController.text);
    }
    else{
      await _service.signUp(_emailController.text, 
                            _passwordController.text);

      }
    }
    on FirebaseAuthException catch(e){
      if(!mounted){
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.message??'Authentication failed!'),
        ),
      );
    }
    catch(e){
      if(!mounted){
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Something went wrong!Please try again!'),
        ),
      );
    }
    finally{
      if(mounted){
        setState(() {
          _isLoading=false;
        });
      }
    }
    
  }
  @override
  void dispose(){
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
        title:const Text("AI Study Assistant"),
      ),
      body:Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Text(_isSignedUp?'Welcome Back!':'Create Account',
                style:Theme.of(context).textTheme.headlineMedium),
                const SizedBox(height:24),
                TextField(
                  controller:_emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration:const InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder( 
                      borderRadius:BorderRadius.all(Radius.circular(12)),
                    ),
                  ),
                ),
                const SizedBox(height:24,),
                TextField(
                  controller:_passwordController,
                  obscureText: true,
                  decoration:const InputDecoration(
                    labelText: 'Password',
                    border:OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(12)),
                    ),
                  ),
                ),
                const SizedBox(height:24),
                SizedBox(
                  width:double.infinity,
                  child:ElevatedButton(onPressed:_isLoading?null:_submit ,
                   child: Text(
                    _isLoading?'Please wait....':
                     _isSignedUp?'Login':'Sign Up',
                    ),
                  ),
                ),
                TextButton(
                  onPressed:_isLoading?null:(){
                    setState(() {
                      _isSignedUp = !_isSignedUp;
                    });
                  },
                  child: Text(
                    _isSignedUp?"Don't have an account?Sign Up":
                    "Already have an account?Log in"
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );

  }
}