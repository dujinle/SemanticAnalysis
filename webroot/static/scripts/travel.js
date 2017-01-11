/**
 * Created by liyongjiang on 2016/5/24.
 */
function GetResult(){
	var intext = document.getElementById("intext");
	if(intext.value.length <= 0 ){
		alert("请输入自然语言");
		intext.focus();
		return false;
	}else if(intext.value.length >= 36){
		alert("输入的内容过长不得超过36字符");
		return false;
	}
	var sptext = document.getElementById("sptext");
	var restext  = document.getElementById("retext");
	sptext.innerText = null;
	restext.innerText = null;
	var jdata = {
		'text':intext.value,
		'mdl':$mdl
	};
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + 'get_result',
		type:'post',
		dataType:'text',
		data:JSON.stringify(jdata),
		success:function(data){
			obj = data;
		},
		error:function(){
			alert(arguments);
		}
	});
	sptext.value = "";
	var json_obj = JSON.parse(obj);
	if(json_obj != null && json_obj.code == 0){
		result = json_obj.result;
		sptext.value = result.inlist;
		restext.value = JSON.stringify(result,null," ");
		return true;
	}else{
		restext.value = json_obj.message.replace(/#/g,'\n');
	}
}
