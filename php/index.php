<?php
$conn = mysqli_connect('localhost', 'root', '', 'airplane');
?>

<!doctype html>
<html lang="en">

<head>
    <title>Title</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="bs/css/bootstrap.min.css">
</head>

<body class="bg-light">
    <div class="container-fluid ">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center">Airplane Status</h1>
            </div>
        </div>
        <br>
        <div class="row">
            <div class=" col-12 " id=data>
                <table class="table table-light table-hover  table-bordered">
                    <thead>
                        <td class="text-center">No</td>
                        <td class="text-center">ICAO</td>
                        <td class="text-center">CallSign</td>
                        <td class="text-center">Latitude</td>
                        <td class="text-center">Longitude</td>
                        <td class="text-center">Altitude</td>
                        <td class="text-center">GroundSpeed</td>
                        <td class="text-center">Heading</td>
                        <td class="text-center">Rate of Climbing</td>
                        <td class="text-center">Live</td>
                    </thead>
                    <?php
$sql = "Select * from airplane ";
$result = $conn->query($sql);
$i = 1;
while ($row = $result->fetch_assoc()) {
    echo '<tr>';
    echo '<td class="text-center">' . $i . '</td>';
    echo '<td class="text-center">' . $row['ICAO'] . '</td>';
    echo '<td class="text-center">' . $row['callsign'] . '</td>';
    echo '<td class="text-center">' . $row['latitude'] . '</td>';
    echo '<td class="text-center">' . $row['longitude'] . '</td>';
    echo '<td class="text-center">' . $row['altitude'] . '</td>';
    echo '<td class="text-center">' . $row['ground_speed'] . '</td>';
    echo '<td class="text-center">' . $row['heading'] . '</td>';
    echo '<td class="text-center">' . $row['rate_of_climb'] . '</td>';
    echo '<td class="text-center">' . $row['live'] . '</td>';
    echo "</tr>";
    $i++;
}

?>




                </table>

            </div>

        </div>
    </div>


    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="bs/js/jquery-3.3.1.min.js"></script>
    <script src="bs/js/popper.min.js"></script>
    <script src="bs/js/bootstrap.min.js"></script>
    <script>
    setInterval(function table() {
        $('#data').load(location.href + ' #data>*')
    }, 2000);
    </script>
</body>

</html>