#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>

/*
gcc snake1.c $(pkg-config -libs -cflags raylib)
./a.out
*/

//Global Variables
int width = 0, height = 0; //window
int snake_x[25], snake_y[15], length, tem_length; //snake
int fruit_x, fruit_y, fruit_x_booster, fruit_y_booster; //fruit
    //state
double speed; 
int position; //position 1 = up, 2 = down, 3 = right, 4 = left
int GameOver;
int newfruit, fruitcheck;
int newfruit_booster, fruitcheck_booster;
int booster;
int live, tem_live;

void InitGame() {
    snake_x[0] = width / 2;
    snake_y[0] = height / 2;
    for (int i = 1; i < width; i++) {
        snake_x[i] = -1;
    }
    for (int i = 1; i < height; i++) {
        snake_y[i] = -1;
    }
    speed = 0.1;
    length = 1;
    position = 3;
    GameOver = 0;
    newfruit = 1;
    fruitcheck = 1;
    newfruit_booster = 1;
    fruitcheck_booster = 1;
    live = 1;
}

void Gameover() {
    GameOver = 1;
    while (!IsKeyPressed(KEY_ENTER)) {
        BeginDrawing();
            ClearBackground(RAYWHITE);
            //void DrawText(const char *text, int posX, int posY, int fontSize, Color color); // Draw text (using default font)
            DrawText("GAME OVER", GetScreenWidth()/2 - MeasureText("GAME OVER", 20)/2, GetScreenHeight()/2 - 50, 20, LIGHTGRAY);
            DrawText("Press Enter to play again", GetScreenWidth()/2 - MeasureText("Press Enter to play again", 10)/2, GetScreenHeight()/2, 10, LIGHTGRAY);
        EndDrawing();
        if (IsKeyPressed(KEY_ESCAPE))   CloseWindow();
    }
    GameOver = 0;
    InitGame();
}

void Win() {
    GameOver = 1;
    while (!IsKeyPressed(KEY_ENTER)) {
        BeginDrawing();
            ClearBackground(LIGHTGRAY);
            //void DrawText(const char *text, int posX, int posY, int fontSize, Color color); // Draw text (using default font)
            DrawText("YOU WIN", GetScreenWidth()/2 - MeasureText("YOU WIN", 20)/2, GetScreenHeight()/2 - 50, 20, RAYWHITE);
            DrawText("Press Enter to play again", GetScreenWidth()/2 - MeasureText("Press Enter to play again", 10)/2, GetScreenHeight()/2, 10, RAYWHITE);
        EndDrawing();
        if (IsKeyPressed(KEY_ESCAPE))    CloseWindow();
    }
    GameOver = 0;
    InitGame();
}

void UpdateDrawGame() {
    if (GameOver == 0) {
        //////////////
        //UpdateGame// 
        //////////////
        
        //Keyboard control
        if (IsKeyDown(KEY_W) && position != 2) {
            position = 1;
        }
        else if (IsKeyDown(KEY_S) && position != 1) {
            position = 2;
        }
        else if (IsKeyDown(KEY_D) && position != 4) {
            position = 3;
        }
        else if (IsKeyDown(KEY_A) && position != 3) {
            position = 4;
        }

        //Snake Movement
            //body
        for (int i = length ; i > 1; i--) {
            snake_x[i-1] = snake_x[i-2];
            snake_y[i-1] = snake_y[i-2];
        }
            //head
        if (position == 1) snake_y[0] -= 1;
        else if (position == 2) snake_y[0] += 1;
        else if (position == 3) snake_x[0] += 1;
        else if (position == 4) snake_x[0] -= 1;
        
        //GameOver--body collision
        for (int i = 1; i < length; i++) {
            if (snake_x[0] == snake_x[i] && snake_y[0] == snake_y[i]) {
                if (live == 1) {
                    WaitTime(0.5);
                    Gameover();
                }
                else {
                    tem_length = length;
                    tem_live = live - 1;
                    GameOver = 1;
                    InitGame();
                    length = tem_length;
                    live = tem_live;
                } 
            }
        }

        //GameOver--wall collision
        if (snake_x[0] < 0 || snake_x[0] >= width || snake_y[0] < 0 || snake_y[0] >= height && live == 1) {
            if (live == 1) {
                WaitTime(0.5);
                Gameover();
            }
            else {
                tem_length = length;
                tem_live = live - 1;
                GameOver = 1;
                InitGame();
                length = tem_length;
                live = tem_live;
            }
        }
        
        //Win--maximum length
        if (length == width * height) {
            WaitTime(0.5);
            Win();
        }

        //Fruit
        if (newfruit == 1) { //create new fruit
            while (1){
                fruit_x = GetRandomValue(0, width - 1);
                fruit_y = GetRandomValue(0, height - 1);
                newfruit = 0;
                for (int i = 0; i < length; i++) {
                        if (fruit_x == snake_x[i] && fruit_y == snake_y[i]) fruitcheck = 0;
                }
                if (fruitcheck == 1) break;
                fruitcheck = 1;
            } 
        }
        
        //Fruit (booster)
        if (newfruit_booster == 1) { //create new fruit
            while (1){
                fruit_x_booster = GetRandomValue(0, width - 1);
                fruit_y_booster = GetRandomValue(0, height - 1);
                newfruit_booster = 0;
                for (int i = 0; i < length; i++) {
                        if (fruit_x_booster == snake_x[i] && fruit_y_booster == snake_y[i]) fruitcheck_booster = 0;
                }
                if (fruitcheck_booster == 1) break;
                fruitcheck_booster = 1;
            } 
        }

        //Fruit collision
        if (snake_x[0] == fruit_x && snake_y[0] == fruit_y) {
            length += 1;
            newfruit = 1;
        }

        //Fruit collision (booster)
        if (snake_x[0] == fruit_x_booster && snake_y[0] == fruit_y_booster) {
            if (length == 1) booster = GetRandomValue(0, 1);
            else booster = GetRandomValue(0, 2);
            newfruit_booster = 1;
            if (booster == 0) { //Speed up
                speed -= 0.03;
            }
            else if (booster == 1) { //Extra life
                live += 1;
            }
            else if (booster == 2) { //Size Reducer
                length -= 1;
            }
        }
        
        ////////////
        //DrawGame//
        ////////////
        BeginDrawing();
            ClearBackground(RAYWHITE);
            for (int i = 0; i <= width; i++) DrawLine(50*i, 0, 50*i, height*50, LIGHTGRAY); // Draw vertical lines
            for (int i = 0; i <= height; i++) DrawLine(0, 50*i, width*50, 50*i, LIGHTGRAY); // Draw horizontal lines
            DrawRectangle(50 * snake_x[0], 50 * snake_y[0], 50, 50, DARKBLUE);
            for (int i = 1; i < length; i++) {
                DrawRectangle(50 * snake_x[i], 50 * snake_y[i], 50, 50, BLUE);
            }
            DrawRectangle(50 * fruit_x, 50 * fruit_y, 50, 50, ORANGE);
            DrawRectangle(50 * fruit_x_booster, 50 * fruit_y_booster, 50, 50, PURPLE);
            if (booster == 0 && newfruit_booster == 1) {
                DrawText("Speed Up", GetScreenWidth()/2 - MeasureText("GAME OVER", 40)/2, GetScreenHeight()/2 - 50, 40, LIGHTGRAY);
                WaitTime(0.7);
            }
            else if (booster == 1 && newfruit_booster == 1) {
                DrawText("Extra Life", GetScreenWidth()/2 - MeasureText("GAME OVER", 40)/2, GetScreenHeight()/2 - 50, 40, LIGHTGRAY);
                WaitTime(0.7);
            }
            else if (booster == 2 && newfruit_booster == 1) {
                DrawText("Size reduced", GetScreenWidth()/2 - MeasureText("GAME OVER", 40)/2, GetScreenHeight()/2 - 50, 40, LIGHTGRAY);
                WaitTime(0.7);
            }
        EndDrawing();
    }
}

int main() {
    //Initialization
    while (width < 5 || width > 25) {
        printf("Please enter the width of the map (between 5 and 25): ");
        scanf("%d", &width);
    }
    while (height < 5 || height > 15) {
        printf("Please enter the height of the map (between 5 and 15): ");
        scanf("%d", &height);
    }

    InitWindow(width * 50, height * 50, "Snake");

    InitGame();

    // Main game loop
    while (!WindowShouldClose())
    {
        UpdateDrawGame();
        WaitTime(speed); // Wait for some time (halt program execution)
    }

    // End game
    CloseWindow();

    return 0;
}