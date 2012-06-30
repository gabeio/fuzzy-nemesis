<!DOCTYPE HTML>
<html itemscope="itemscope" itemtype="http://schema.org/WebPage">
	<head>
		<meta charset="UTF-8">
		<script src="/static/jq.js"></script>
		<title>WebSocket Chat</title>
	</head>
	<body>
		<div style="text-align:center">
			<label>Manager password:<input id="pass" type="password"></label><input id="submit" type="button" value="submit"/>
		</div>
		<form id="goto"></form>
		<script>
			$(function(){
				$("#nick").change(function(){go();});
                               $("#submit").click(function(){go();});
                               function go(){
                                   goto.action=$("#nick").val();
                                   goto.submit();
                               }
			});
		</script>
	</body>
</html>