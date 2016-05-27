/**
 * Created by liyongjiang on 2016/5/24.
 */
//这些是测试函数
function analyse() {
    alert("analyse");
}
function add_ut() {
	ut_obj = document.getElementById('ut_text');
	ut_scope_obj = document.getElementById('ut_scope');
	ut_attr_obj = document.getElementsByName('ut_attr');

	ut_value = ut_obj.value;
	ut_scope = ut_scope_obj.value;
	ut_attr = [];
	for(var i = 0;i < ut_attr_obj.length;i++){
		if(ut_attr_obj[i].checked){
			ut_attr.push(ut_attr_obj[i].value);
		}
	}
	idata = new Object();
	idata.type = 'UT';
	idata.mdl = $mdl;
	idata.value = ut_value;
	idata.scope = ut_scope;
	idata.attr = ut_attr;

	$.ajax({
		async:false,
		url: $basepath + 'add',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}
function del(type,vid) {
	v_obj = document.getElementById(vid);
	v_value = v_obj.value;

	idata = new Object();
	idata.type = type;
	idata.value = v_value;
	idata.mdl = $mdl;

	$.ajax({
		async:false,
		url: $basepath + 'del',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}
function get(type) {
	idata = new Object();
	idata.type = type;
	idata.mdl = $mdl;

	$.ajax({
		async:false,
		url: $basepath + 'get',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	if(obj != null && obj.code == 0){
		y.value = JSON.stringify(obj.result,null,' ');
	}else{
		y.value = obj.message.replace(/#/g,'\n');
	}
}

function add_nt() {
	nt_obj = document.getElementById('nt_text');
	nt_scope_obj = document.getElementById('nt_scope');
	nt_interval_obj = document.getElementById('nt_interval');
	nt_type_obj = document.getElementsByName('nt_type');

	nt_value = nt_obj.value;
	nt_scope = nt_scope_obj.value;
	nt_interval = nt_interval_obj.value;
	nt_type = null;

	for(var i = 0;i < nt_type_obj.length;i++){
		if(nt_type_obj[i].checked){
			nt_type = nt_type_obj[i].value;
			break;
		}
	}
	idata = new Object();
	idata.type = 'NT';
	idata.mdl = $mdl;
	idata.value = nt_value;
	idata.scope = nt_scope;
	idata.interval = nt_interval;
	idata.nt_type = nt_type;

	$.ajax({
		async:false,
		url: $basepath + 'add',
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	y.value = obj.message.replace(/#/g,'\n');
}

function add_word(){
    alert("add_word");
}
function del_word(){
    alert("del_word");
}
function save_word(){
    alert("save_word");
}
//这个是功能描述的函数
function describe( dum) {
    if (dum == "tu-describe") {
        document.getElementById("showText").innerHTML = "时间单位:对数字时间的一个单位，如：年、月、日、时、分、秒。\n 举例如：2016年5月25日16时57分30秒，中的年、月、日、时、分、秒都是单位，这些都是时间类型，3周的周就是数量单位"
    }
    else if (dum == "td-describe") {
        document.getElementById("showText").innerHTML = "时间修饰：对时间的一个修饰，如上月，昨天，明天中的上、昨、明，都是对时间的修饰。\n 区间：为修饰一个区间判断，是多长时间，如昨天就是[-1,0],明天是[1,2]"
    }
    else if (dum == "cd-describe") {
        document.getElementById("showText").innerHTML = "综合修饰："
    }
    else if (dum == "tr-describe") {
        document.getElementById("showText").innerHTML = "时间频率：就是对时间发生的频率的描述，如 每天、经常、偶尔、总，都是频率，且频率为高、中、低、频率"
    }
    else if (dum == "bs-describe") {
        document.getElementById("showText").innerHTML = "事情状态："
    }
    else if (dum == "ts-describe") {
        document.getElementById("showText").innerHTML = "时间状态："
    }

}
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

function DealWords(type,action,vid,did){
	dcom = null;vcom = null;
	var idata = new Object();
	if(action != 'get'){
		if(did != null){
			dcom = document.getElementsByName(did);
		}
		if(vid != null){
			vcom = document.getElementById(vid);
		}
		if(vcom != null && vcom.value.length <= 0){
			vcom.focus();
			return false;
		}
		idata.value = vcom.value;
	}
	dir = null;
	if(dcom != null){
		for(var i = 0;i < dcom.length;i++){
			if(dcom[i].checked){
				dir = dcom[i].value;
				break;
			}
		}
	}
	idata.type = type;
	idata.mdl = $mdl;
	if(dir != null){
		idata.dir = dir;
	}
	var obj = null;
	$.ajax({
		async:false,
		url: $basepath + action,
		type:"post",
		data:JSON.stringify(idata),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
		}
	});
	y = document.getElementById('status_id');
	if(obj != null && obj.code == 0){
		if(action == 'get'){
			y.innerText = JSON.stringify(obj.result,null,' ');
		}else{
			y.innerText = obj.message.replace(/#/g,'\n');
		}
	}else{
		y.innerText = obj.message.replace(/#/g,'\n');
	}
	return false;
}

function save_data(mdl){
	var obj = null;
	data = {
		'mdl':mdl
	};
	$.ajax({
		async:false,
		url: $basepath + 'save_data',
		type:'post',
		dataType:"text",
		data:JSON.stringify(data),
		success:function(data){
			obj = data;
		},
		error:function(){
			alert(arguments);
		}
	});
	sptext.value = "";
	var json_obj = JSON.parse(obj);
	y = document.getElementById('status_id');
	y.value = json_obj.message.replace(/#/g,'\n');
}
