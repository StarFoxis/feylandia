const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
const audio = new Audio();
const keys = $('.key').hide();

let matrix = [];
let tractors = [];

let timeout = 0;
let flag = false;

let padding = 15,
    canvas_width = 735,
    canvas_height = 735,
    cube_count = 11,
    cube_size = (canvas_width-padding*2)/cube_count;

let tractor_num = 1;

let player = {
    x: 0,
    y: 0
}

function createMatrix() {
    // x x x
    // 0 0 0 y
    // 0 0 0 y
    // 0 0 0 y
    matrix = [];
    for (let y=0; y<cube_count; y++) {
        row = []
        for (let x=0; x<cube_count; x++) {
            row.push(false)
        }
        matrix.push(row)
    }
}

function createTractor(num) {
    tractors = [];
    for (let i=0; i<num; i++) {
        tractors.push({
            x: 0,
            y: 0
        })
    }
}

async function createMaze() {
    flag = false;
    canvas.width = canvas_width;
    canvas.height = canvas_height;
    ctx.beginPath();
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas_width, canvas_width);

    while (validMatrix()) {
        for (let tractor of tractors) {
            moveTractor(tractor);
        }

        drawMatrix();

        // for (let tractor of tractors) {
        //     drawTractor(tractor);
        // }

        await delay(timeout);
    } 
    flag = true;
    keys.show();
    drawMaze(); 
    drawPlayer();
}

function moveTractor(tractor) {
    let move = [];

    if (tractor.x > 0) move.push([-2, 0]);
    if (tractor.x < cube_count-1) move.push([2, 0]);

    if (tractor.y > 0) move.push([0, -2]);
    if (tractor.y < cube_count-1) move.push([0, 2]);

    let [dx, dy] = getRandomItem(move);
    tractor.x += dx;
    tractor.y += dy;

    if (!matrix[tractor.x][tractor.y]) {
        matrix[tractor.x-dx/2][tractor.y-dy/2] = true;
        matrix[tractor.x][tractor.y] = true;
    }
}

function drawMatrix() {
    for (let y=0; y<cube_count; y++) {
        for (let x=0; x<cube_count; x++) {
            ctx.beginPath();
            ctx.fillStyle = matrix[x][y] ? 'white' : 'black';
            ctx.fillRect(x*cube_size+padding, y*cube_size+padding, cube_size, cube_size); 
        }
    }
}

function drawTractor(tractor) {
    colors = ['red', 'blue', 'green', 'yellow', 'pink', 'gray', 'purple', 'violet'];
    let tractor_padding = 1;
    ctx.beginPath();
    ctx.fillStyle = getRandomItem(colors);
    ctx.fillRect(tractor.x*cube_size+padding+tractor_padding, tractor.y*cube_size+padding+tractor_padding, cube_size-tractor_padding*2, cube_size-tractor_padding*2);
}

function drawMaze() {
    drawMatrix();
    
    ctx.beginPath()
    ctx.fillStyle = 'green';
    ctx.fillRect(padding, padding, cube_size, cube_size); 

    ctx.beginPath()
    ctx.fillStyle = 'yellow';
    ctx.fillRect((cube_count-1)*cube_size+padding, (cube_count-1)*cube_size+padding, cube_size, cube_size); 
}

function validMatrix() {
    for (let y=0; y<cube_count; y+=2) {
        for (let x=0; x<cube_count; x+=2) {
            if (!matrix[x][y]) 
                return true;
        }
    }
    return false;
}

function drawPlayer() {
    let diam = cube_size/2,
        x = player.x*cube_size+padding+diam,
        y = player.y*cube_size+padding+diam;

    ctx.beginPath();
    ctx.fillStyle = 'purple';
    ctx.arc(x, y, diam, 0, Math.PI*2);
    ctx.fill();
}

function validPlayerMove(keyCode) {
    switch (keyCode) {
        case 87:
            if (matrix[player.x][player.y-1])
                player.y--;
            break;
        case 83:
            if (matrix[player.x][player.y+1])
                player.y++
            break;
        case 65:
            if (matrix[player.x-1] && matrix[player.x-1][player.y])
                player.x--;
            break;
        case 68:
            if (matrix[player.x+1] && matrix[player.x+1][player.y])
                player.x++;
            break;
    }
    playerWins();
    drawMaze();
    drawPlayer();
}

function playerWins() {
    if (matrix.length > 50) {
        drawHorrorFace();
        keys.hide();
    }
    else if (player.x == matrix.length-1 && player.y == matrix.length-1) {
        cube_count += 6;
        cube_size = (canvas_width-padding*2)/cube_count;
        createMatrix();
        tractor_num += 5;
        createTractor(tractor_num);
        createMaze();
        player.x = 0;
        player.y = 0;
        drawMaze();
        drawPlayer();
        keys.hide();
    }
}

function autoPlayerWins() {
    player.x = matrix.length-1;
    player.y = matrix.length-1;
    playerWins();
}

function drawHorrorFace() {
    flag = false;
    let horror = new Image();
    audio.src = '/static/music/horror.mp3';
    audio.loop = false;
    horror.src = '/static/images/horror.png';
    horror.onload = function() {
        ctx.drawImage(horror, 0, 0, canvas_width, canvas_height);
    }
}

function getRandomItem(array) {
    let index = Math.floor(Math.random()*array.length)
    return array[index]
}

function delay(timeout) {
    return new Promise((resolve) => setTimeout(resolve, timeout));
}

function bg_music() {
    audio.src = '/static/music/play.mp3';
    audio.autoplay = true;
    audio.loop = true;
}

function main() {
    createMatrix();
    createTractor(tractor_num);
    matrix[0][0] = true;
    createMaze();

    bg_music();
}

document.onkeydown = function(event) {
    // up - 87
    // down - 83
    // left - 65
    // right - 68
    let wasd = [87, 83, 65, 68]
    if (wasd.includes(event.keyCode) && flag) validPlayerMove(event.keyCode);
    if (event.keyCode == 19 && flag) autoPlayerWins();
}

main();