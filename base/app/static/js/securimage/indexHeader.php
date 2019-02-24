<?php session_start();
	if(!isset($_SESSION['name']) or (!isset($_SESSION['password'])) or $_SESSION['name'] == '' or $_SESSION['password'] == '')
	{
		header('Location: login.php');
	}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Firefly Infotech</title>
<link rel="stylesheet" type="text/css" href="admin.css">
<script>
//get date from http://stackoverflow.com/questions/12409299/how-to-get-current-formatted-date-dd-mm-yyyy-in-javascript-and-append-it-to-an-i
//get time from http://www.w3schools.com/js/tryit.asp?filename=tryjs_timing_clock
function startTime() {
    var today=new Date();
    var h=today.getHours();
    var m=today.getMinutes();
    var s=today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);

    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!

    var yyyy = today.getFullYear();
    if(dd<10){
        dd='0'+dd
    } 
    if(mm<10){
        mm='0'+mm
    } 

    document.getElementById('date').innerHTML = dd+'/'+mm+'/'+yyyy;
    document.getElementById('time').innerHTML = h+":"+m+":"+s;
    var t = setTimeout(function(){startTime()},500);
}

function checkTime(i) {
    if (i<10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}

//create a stick nav
$(window).bind('scroll', function() {
         if ($(window).scrollTop() > 50) {
             $('#navMenu').addClass('fixed');
         }
         else {
             $('#navMenu').removeClass('fixed');
         }
    });
</script>
</head>

<body onload="startTime()">
<?php $dbid = $_SESSION['name'];
	$access = $_SESSION['type'];
	?>	
<div id="wrapper">
<div id="headerbg">
  <div id="role"><p class="LABEL">Logged in as <b>
  <?php if ($access == "superadmin") {
	  echo "Super Administrator";
  } elseif ($access == "staffMgr") {
	  echo "Manager";
  } elseif ($access == "staffEgr") {
	  echo "Engineer";
  } elseif ($access == "staff") {
	  echo "Staff";
  } elseif ($access == "customer") {
	  echo "Customer";
  }?></b>.</p></div>
</div> 
<nav>
		<ul style="width:960px; margin-top:-15px; margin-left:170px; z-index:5;">
				
			<li><a href="index.html">Home</a></li>
			<li><a href="about.html">About Global Hearts</a>
				<ul>
					<li><a href="index.php.html">Mentally Disadvantaged</a></li>
					<li><a href="pd.html">Physically Disadvantaged</a></li>
					<li><a href="sd.html">Income Inequality Disadvantaged</a></li>
					<li><a href="ed.html">Education Disadvantaged</a></li>
					<li><a href="emd.html">Employment Disadvantaged</a></li>
				</ul>
			</li>
			<li><a href="chatbox.html">Chat Box</a></li>
			<li><a href="main.php">Gallery</a></li>
			<li><a href="donation form.html">Donation</a>
			<li><a href="event.html">Events</a>
				  
		


<ul>
<li><a class="BANNER" href="index.php">Home</a>
</li> <!-- end main LI -->
</ul> <!-- end main UL -->


<ul>
<li><a class="BANNER" href="#">Account Management</a>
	<ul>
      <?php
	  if ($_SESSION['type'] == "customer"){
		  
		  ?>
<li><a class="BANNERITEMS" href="profile.php">Update Profile</a></li>
      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staff" or $_SESSION['type'] == "staffEgr" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<li><a class="BANNERITEMS" href="staffprofile.php">Update Profile</a></li>
      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<li><a class="BANNERITEMS" href="register.php">Create Staff</a></li>
      <?php }?>
<li><a class="BANNERITEMS" href="change_password.php">Change Password</a></li>
      <?php
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffMgr") {		  
		  ?>
<li><a class="BANNERITEMS" href="change_staff_password.php">Reset Staff Password</a></li>
      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staff" or $_SESSION['type'] == "staffEgr" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<li><a class="BANNERITEMS" href="allcustomer.php">All Customers</a></li>
<li><a class="BANNERITEMS" href="allstaff.php">All Staff</a></li>
      <?php }?>
	</ul> <!-- end inner UL -->
</li> <!-- end main LI -->
</ul> <!-- end main UL -->


<ul>
<li><a class="BANNER" href="#">Service Request</a>
	<ul>
      <?php
	  if ($_SESSION['type'] == "customer"){
		  
		  ?>
<li><a class="BANNERITEMS" href="createcase.php">Create</a></li>
<li><a class="BANNERITEMS" href="casehistory.php">History</a></li>
      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staff" or $_SESSION['type'] == "staffEgr" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<li><a class="BANNERITEMS" href="allcases.php">View All</a></li>
      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffEgr"){
		  
		  ?>
<?php //<li><a class="BANNERITEMS" href="createcustcase.php">Create</a></li> ?>
<li><a class="BANNERITEMS" href="caseaction.php">Edit</a></li>
      <?php }

	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<li><a class="BANNERITEMS" href="caseassign.php">Allocate Engineer</a></li>
      <?php }?>
	</ul> <!-- end inner UL -->
</li> <!-- end main LI -->
</ul> <!-- end main UL -->

      <?php
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<ul>
<li><a class="EBANNER" href="#">Billing</a>
	<ul>
<li><a href="#"></a></li>
<li><a href="#"></a></li>
	</ul> <!-- end inner UL -->
</li> <!-- end main LI -->
</ul> <!-- end main UL -->

      <?php }
	  if ($_SESSION['type'] == "superadmin" or $_SESSION['type'] == "staffMgr"){
		  
		  ?>
<ul>
<li><a class="BANNER" href="#">Reports</a>
	<ul>
<li><a class="BANNERITEMS" href="reportbycase.php">By Engineer</a></li>
<li><a href="#"></a></li>
	</ul> <!-- end inner UL -->
</li> <!-- end main LI -->
</ul> <!-- end main UL -->
      <?php } ?>

<ul>
<li><a class="BANNER" href="logout_now.php">Logout</a>
</li> <!-- end main LI -->
</ul> <!-- end main UL -->


</div> <!-- end navMenu -->
</div> <!-- end wrapper div -->

<div id="footerbg">
  <div id="content">
  <table width="100%" border="0" align="center">
  <tr>
    <td width="899">