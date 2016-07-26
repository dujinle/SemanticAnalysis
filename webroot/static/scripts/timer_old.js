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
	ut_reg_obj = document.getElementById('ut_match');

	ut_value = ut_obj.value;
	ut_scope = ut_scope_obj.value;
	ut_reg = ut_reg_obj.value;
	var counter=0;
	ut_attr = [];
	for(var i = 0;i < ut_attr_obj.length;i++){
		if(ut_attr_obj[i].checked){
			ut_attr.push(ut_attr_obj[i].value);
			counter++;
		}
	};
	if(ut_value==""){
		alert("未输入内容，请输入！")
		return
	};
	if(document.getElementsByName("ut_scope")[0].selectedIndex==0){
		alert("未选择年月日，请选择单位！")
		return
	};
	if(counter==0){
		alert("未选择类型，请选择类型！")
		return
	};
	idata = new Object();
	idata.type = 'UT';
	idata.mdl = $mdl;
	idata.value = ut_value;
	idata.scope = ut_scope;
	idata.attr = ut_attr;
	idata.reg = ut_reg;
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
	nt_func_type = document.getElementsByName('func_type');
	nt_obj = document.getElementById('nt_text');
	nt_scope_obj = document.getElementById('nt_scope');
	nt_interval_obj = document.getElementById('nt_interval');
	nt_type_obj = document.getElementsByName('nt_type');

	nt_value = nt_obj.value;
	nt_scope = nt_scope_obj.value;
	nt_interval = nt_interval_obj.value;
	nt_type = null;

	var counter_type=0;
	for(var i = 0;i < nt_type_obj.length;i++){
		if(nt_type_obj[i].checked){
			nt_type = nt_type_obj[i].value;
			counter_type++;
			break;
		}
	};
	var nt_func = null;
	var counter_func=0;
	for (var i = 0;i < nt_func_type.length;i++){
		if(nt_func_type[i].checked){
			nt_func = nt_func_type[i].value;
			counter_func++;
			break;
		}
	};
	if(nt_value==""){
		alert("未输入内容，请输入！")
		return
	};
	if(nt_interval==""){
		alert("未输入区间，请输入！")
		return
	};
	if(document.getElementsByName("nt_scope")[0].selectedIndex==0){
		alert("未选择年月日，请选择单位！")
		return
	};
	if(counter_func==0){
		alert("未选择方法，请选择方法！")
		return
	};
	idata = new Object();
	idata.type = 'NT';
	idata.mdl = $mdl;
	idata.value = nt_value;
	idata.scope = nt_scope;
	idata.interval = nt_interval;
	idata.nt_type = nt_type;
	idata.func = nt_func;

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
//这个是TR函数
function add_rt() {
	rt_sel = document.getElementsByName('tr-sel');
	rt_obj = document.getElementById('tr');

	rt_value = rt_obj.value;
	rt_level = null;
	var counter_type=0;
	for(var i = 0;i < rt_sel.length;i++){
		if(rt_sel[i].checked){
			rt_level = rt_sel[i].value;
			counter_type++;
			break;
		}
	};
	if(rt_value==""){
		alert("未输入内容，请输入！")
		return
	};

	if(counter_type==0){
		alert("未选择等级，请选择等级！")
		return
	};
	idata = new Object();
	idata.type = 'TM';
	idata.mdl = $mdl;
	idata.value = rt_value;
	idata.level = rt_level;

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

//这个是BS函数
function add_bs() {
	bs_sel = document.getElementsByName('bs-sel');
	bs_obj = document.getElementById('bs');

	bs_value = bs_obj.value;
	bs_status = null;
	var counter_type=0;
	for(var i = 0;i < bs_sel.length;i++){
		if(bs_sel[i].checked){
			bs_status = bs_sel[i].value;
			counter_type++;
			break;
		}
	};
	if(bs_value==""){
		alert("未输入内容，请输入！")
		return
	};

	if(counter_type==0){
		alert("未选择状态，请选择状态！")
		return
	};
	idata = new Object();
	idata.type = 'AS';
	idata.mdl = $mdl;
	idata.value = bs_value;
	idata.status = bs_status;

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

//这个是TS函数
function add_ts() {
	ts_sel = document.getElementsByName('ts-sel');
	ts_obj = document.getElementById('ts');

	ts_value = ts_obj.value;
	ts_status = null;
	var counter_type=0;
	for(var i = 0;i < ts_sel.length;i++){
		if(ts_sel[i].checked){
			ts_status = ts_sel[i].value;
			counter_type++;
			break;
		}
	};
	if(ts_value==""){
		alert("未输入内容，请输入！")
		return
	};

	if(counter_type==0){
		alert("未选择状态，请选择状态！")
		return
	};
	idata = new Object();
	idata.type = 'TS';
	idata.mdl = $mdl;
	idata.value = ts_value;
	idata.status = ts_status;

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
//这个是功能描述的函数
function describe( dum) {
    if (dum == "tu-describe") {
        document.getElementById("status_id").value = "时间单位:对数字时间的一个单位，如：年、月、日、时、分、秒。\n 举例如：2016年5月25日16时57分30秒，中的年、月、日、时、分、秒都是单位，这些都是时间类型，3周的周就是数量单位"
    }
    else if (dum == "td-describe") {
        document.getElementById("status_id").value = "时间修饰：对时间的一个修饰，如上月，昨天，明天中的上、昨、明，都是对时间的修饰。\n 区间：为修饰一个区间判断，是多长时间，如昨天就是[-1,0],明天是[1,2]"
    }
    else if (dum == "cd-describe") {
        document.getElementById("status_id").value = "综合修饰："
    }
    else if (dum == "tr-describe") {
        document.getElementById("status_id").value = "时间频率：就是对时间发生的频率的描述，如 每天、经常、偶尔、总，都是频率，且频率为高、中、低、频率"
    }
    else if (dum == "bs-describe") {
        document.getElementById("status_id").value = "事情状态："
    }
    else if (dum == "ts-describe") {
        document.getElementById("status_id").value = "时间状态："
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
			y.value = JSON.stringify(obj.result,null,' ');
		}else{
			y.value = obj.message.replace(/#/g,'\n');
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
