<?php
$galleryDir = 'Gallery';  // relative to /var/www/html
$images = glob($galleryDir . "/*.jpg");
?>

<!DOCTYPE html>
<html>
<head>
    <title>Gallery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #ffffff;
            text-align: center;
        }
        .gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            padding: 20px;
        }
        .image-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .image-container img {
            max-width: 300px;
            height: auto;
            border: 1px solid #ccc;
        }
        .filename {
            margin-top: 5px;
            font-size: 14px;
            color: #333;
            word-break: break-word;
        }
    </style>
</head>
<body>

<h1>Snapshot Gallery</h1>
<div class="gallery">
    <?php
    if (empty($images)) {
        echo "<p>No snapshots yet!</p>";
    } else {
        // Sort images by newest first
        rsort($images);
        foreach ($images as $img) {
            $filename = basename($img);
            echo "<div class='image-container'>";
            echo "<img src='$img' alt='Snapshot'>";
            echo "<div class='filename'>$filename</div>";
            echo "</div>";
        }
    }
    ?>
</div>

</body>
</html>
