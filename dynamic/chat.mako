<!DOCTYPE HTML>
<html itemscope="itemscope" itemtype="http://schema.org/WebPage">
	<head>
		<meta charset="UTF-8">
		<script src="/static/jq.js"></script>
		<script src="/static/jq.ws.js"></script>
		<script src="http://jquery-json.googlecode.com/files/jquery.json-2.2.min.js"></script>
		<title>WebSocket Chat</title>
		<script>
			var loc=location.hostname;
			var path=location.pathname.split("/");
        	if (loc=="localhost") //## change this before you production this server!
            	loc=loc+":1025";
			%if nick=="Managers":
			var ws=$.websocket("ws://"+loc+"/"+path[1]+"/"+path[2],{
			%else:
	        var ws=$.websocket("ws://"+loc+"/"+path[1],{
	        %endif
    	        events:{
					%if nick:
					connect:function(e) {
					ws.send('message',{'me':'${nick}'});
					},
				    %endif
        	        message:function(e) {
						if(e.data.nick && e.data.message) {
							%if nick!="Managers":
							if(e.data.to==$("#nick").val()){
							%endif
								$('#messagebox').append(
									%if nick=="Managers":
									'<div class="chatline"><span class="nick">&lt;<b onclick="to(this.innerHTML)">' +e.data.nick + '</b>&gt;</span>' +
									%else:
									'<div class="chatline"><span class="nick">&lt;<b>' + e.data.nick + '</b>&gt;</span>' +
									%endif
									%if nick=="Managers":
									'<span class="to">&lt;' + e.data.to + '&gt;</span>'+
									%endif
									'<span class="message"> ' + e.data.message + '</span></div>');
								document.getElementById('messagebox').scrollTop = 9999999;
							%if nick!="Managers":
							}
							%endif
						}
					}
				}
			});
			%if nick=="Managers":
			function to(val){
				document.getElementById('to').value=val;
				$("#message").focus();
			}
			%endif
			function goodbye(){
				document.getElementById("to").value="Managers";
				document.getElementById("message").value="<Signed off>";
				$("#send").click();
			}
			function wsms() {
				ws.send('message', {
					'to' : $('#to').val(),
					'nick' : $('#nick').val(),
					'message' : $('#message').val(),
				});
				%if nick!="Managers":
				if($("#message").val()!=""){
					$('#messagebox').append(
						'<div class="chatline"><span class="nick"><b>&lt;' + $("#nick").val() + '&gt;</b></span>' +
						##if nick=="Managers":
						##'<span class="to">&lt;' + $("#to").val() + '&gt;</span>'+
						##endif
						'<span class="message">' + $("#message").val() + '</span></div>');
					document.getElementById('messagebox').scrollTop = 9999999;
				}
				%endif
				$('#message').val('');
				$('#message').focus();
            }
			$(function() {
				$('#send').click(function(){wsms();});
				$('#message').keyup(function(evt){if(evt.keyCode==13)$('#send').click();});
			});
		</script>
		<style>
			#messagebox {
				position:fixed;
				top:10px;
				left:10px;
				right:10px;
				bottom:33px;
				overflow:auto;
				/*border:1px solid #000;*/
			}#controlbox {
				position:fixed;
				bottom:10px;
				left:10px;
				right:10px;
			}#message {
				width:400px;
			}
		</style>
	</head>
	<body onunload="goodbye();">
		<span id="keycode"></span>
		<div id="messagebox">
		</div>
		<div id="controlbox">
			%if nick=="Managers":
			<input type="text" id="to" value=""/>
			%else:
			<input type="hidden" id="to" value="Managers"/>
			%endif
			%if nick:
			<input type="hidden" id="nick" value="${nick}"/>
			%else:
			<input type="text" id="nick"/>
			%endif
			<input type="text" id="message"/>
			<input type="button" id="send" onclick="wsms();" value="<Send>"/>
		</div>
	</body>
</html>