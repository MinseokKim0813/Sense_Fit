
function b64DecodeUnicode(str) {
    return decodeURIComponent(Array.prototype.map.call(atob(str), function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

document.getElementById('csv-file').style.display = 'block';
document.getElementById('csv-file').style.margin = 'auto';
document.getElementById('csv-file').style.marginBottom = '10px';

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.style.display = 'block';
canvas.style.margin = 'auto';

ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = "black";
ctx.strokeWidth = 1;

const reader = new FileReader();

reader.addEventListener('load', (event) => {
    const result_base_64 = event.target.result;
    const result_decoded = b64DecodeUnicode(result_base_64.split(',')[1]);

    const dataPoints = result_decoded.split('\n').map(line => {
        const [timestamp, x, y, clicked] = line.split(',');
        return { x: parseInt(x), y: parseInt(y), clicked: clicked === '1' };
    });

    console.log(dataPoints)
    ctx.beginPath();
    ctx.moveTo(dataPoints[0].x, dataPoints[0].y);



    for (const point of dataPoints) {
        ctx.lineTo(point.x, point.y);
    }

    ctx.stroke();
});

document.getElementById('csv-file').addEventListener('change', (event) => {
    reader.readAsDataURL(event.target.files[0]);
});