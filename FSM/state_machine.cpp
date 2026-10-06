#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <chrono>
#include <cmath>

using namespace std;

// =====================================================
// GRID SIZE
// =====================================================

const int SIZE = 20;


// =====================================================
// ROVER STATES
// =====================================================

enum RoverState
{
    MOVING,
    AVOIDING,
    REACHED,
    STOPPED
};


// =====================================================
// DIRECTIONS
// =====================================================

enum Direction
{
    UP,
    RIGHT,
    DOWN,
    LEFT
};


// =====================================================
// POSITION
// =====================================================

struct Position
{
    int x;
    int y;
};


// =====================================================
// CHECK TWO POSITIONS
// =====================================================

bool samePosition(Position a, Position b)
{
    return a.x == b.x && a.y == b.y;
}


// =====================================================
// CHECK GRID BOUNDARY
// =====================================================

bool isInsideGrid(int x, int y)
{
    return x >= 0 && x < SIZE &&
           y >= 0 && y < SIZE;
}


// =====================================================
// CHECK OBSTACLE
// =====================================================

bool isObstacle(int x, int y,
                const vector<Position>& obstacles)
{
    for (const auto& obstacle : obstacles)
    {
        if (obstacle.x == x && obstacle.y == y)
        {
            return true;
        }
    }

    return false;
}


// =====================================================
// CHECK WHETHER POSITION IS IN PATH
// =====================================================

bool isInPath(Position position,
              const vector<Position>& path)
{
    for (const auto& point : path)
    {
        if (samePosition(position, point))
        {
            return true;
        }
    }

    return false;
}


// =====================================================
// SHOW DIRECTION
// =====================================================

void showDirection(Direction direction)
{
    switch (direction)
    {
        case UP:
            cout << "UP";
            break;

        case RIGHT:
            cout << "RIGHT";
            break;

        case DOWN:
            cout << "DOWN";
            break;

        case LEFT:
            cout << "LEFT";
            break;
    }
}


// =====================================================
// GET DIRECTION BETWEEN TWO CELLS
// =====================================================

Direction getDirection(Position current,
                        Position next)
{
    if (next.x > current.x)
        return RIGHT;

    if (next.x < current.x)
        return LEFT;

    if (next.y > current.y)
        return UP;

    return DOWN;
}


// =====================================================
// BFS PATH FINDING
// =====================================================

bool findPath(Position start,
              Position target,
              const vector<Position>& obstacles,
              vector<Position>& path)
{
    bool visited[SIZE][SIZE] = {};

    Position parent[SIZE][SIZE];

    queue<Position> q;

    q.push(start);

    visited[start.x][start.y] = true;

    // Four possible movements:
    // Right, Left, Up, Down

    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};

    while (!q.empty())
    {
        Position current = q.front();
        q.pop();

        // Target reached
        if (samePosition(current, target))
        {
            break;
        }

        for (int i = 0; i < 4; i++)
        {
            int nx = current.x + dx[i];
            int ny = current.y + dy[i];

            // Check grid
            if (!isInsideGrid(nx, ny))
            {
                continue;
            }

            // Check obstacle
            if (isObstacle(nx, ny, obstacles))
            {
                continue;
            }

            // Check already visited
            if (visited[nx][ny])
            {
                continue;
            }

            visited[nx][ny] = true;

            parent[nx][ny] = current;

            q.push({nx, ny});
        }
    }


    // No path exists
    if (!visited[target.x][target.y])
    {
        return false;
    }


    // =================================================
    // REBUILD PATH
    // =================================================

    Position current = target;

    while (!samePosition(current, start))
    {
        path.push_back(current);

        current = parent[current.x][current.y];
    }

    path.push_back(start);


    // Reverse path
    vector<Position> reversedPath;

    for (int i = path.size() - 1; i >= 0; i--)
    {
        reversedPath.push_back(path[i]);
    }

    path = reversedPath;

    return true;
}


// =====================================================
// DISPLAY GRID
// =====================================================

void displayGrid(Position rover,
                 Position target,
                 Direction direction,
                 const vector<Position>& obstacles,
                 const vector<Position>& travelledPath)
{
    cout << "\n";

    for (int y = SIZE - 1; y >= 0; y--)
    {
        for (int x = 0; x < SIZE; x++)
        {
            Position current = {x, y};


            // Rover
            if (samePosition(current, rover))
            {
                switch (direction)
                {
                    case UP:
                        cout << "^ ";
                        break;

                    case RIGHT:
                        cout << "> ";
                        break;

                    case DOWN:
                        cout << "v ";
                        break;

                    case LEFT:
                        cout << "< ";
                        break;
                }
            }


            // Target
            else if (samePosition(current, target))
            {
                cout << "G ";
            }


            // Obstacle
            else if (isObstacle(x, y, obstacles))
            {
                cout << "# ";
            }


            // Travelled path
            else if (isInPath(current, travelledPath))
            {
                cout << "* ";
            }


            // Empty
            else
            {
                cout << ". ";
            }
        }

        cout << endl;
    }
}


// =====================================================
// MAIN
// =====================================================

int main()
{
    vector<Position> obstacles;

    Position rover;
    Position target;

    vector<Position> path;
    vector<Position> travelledPath;


    // =================================================
    // TITLE
    // =================================================

    cout << "=============================================\n";
    cout << "        ROVER FSM PATH SIMULATOR\n";
    cout << "=============================================\n";

    cout << "\nGrid Size: 20 x 20\n";


    // =================================================
    // NUMBER OF OBSTACLES
    // =================================================

    int numberOfObstacles;

    cout << "\nEnter number of obstacles: ";
    cin >> numberOfObstacles;


    // =================================================
    // OBSTACLE COORDINATES
    // =================================================

    for (int i = 0; i < numberOfObstacles; i++)
    {
        Position obstacle;

        cout << "\nObstacle " << i + 1 << endl;

        cout << "Enter X coordinate (0-19): ";
        cin >> obstacle.x;

        cout << "Enter Y coordinate (0-19): ";
        cin >> obstacle.y;


        // Check coordinate
        if (!isInsideGrid(obstacle.x, obstacle.y))
        {
            cout << "Invalid coordinate!\n";
            i--;
            continue;
        }


        // Prevent duplicate obstacle
        if (isObstacle(obstacle.x,
                       obstacle.y,
                       obstacles))
        {
            cout << "Obstacle already exists!\n";
            i--;
            continue;
        }


        obstacles.push_back(obstacle);
    }


    // =================================================
    // ROVER START POSITION
    // =================================================

    cout << "\n=============================================\n";
    cout << "           ROVER START POSITION\n";
    cout << "=============================================\n";

    cout << "Enter rover X position (0-19): ";
    cin >> rover.x;

    cout << "Enter rover Y position (0-19): ";
    cin >> rover.y;


    // Check rover position
    if (!isInsideGrid(rover.x, rover.y))
    {
        cout << "\nInvalid rover position!\n";
        return 0;
    }


    // Rover cannot start on obstacle
    if (isObstacle(rover.x,
                   rover.y,
                   obstacles))
    {
        cout << "\nRover cannot start on an obstacle!\n";
        return 0;
    }


    // =================================================
    // TARGET POSITION
    // =================================================

    cout << "\n=============================================\n";
    cout << "            TARGET POSITION\n";
    cout << "=============================================\n";

    cout << "Enter target X coordinate (0-19): ";
    cin >> target.x;

    cout << "Enter target Y coordinate (0-19): ";
    cin >> target.y;


    // Check target position
    if (!isInsideGrid(target.x, target.y))
    {
        cout << "\nInvalid target position!\n";
        return 0;
    }


    // Target cannot be obstacle
    if (isObstacle(target.x,
                   target.y,
                   obstacles))
    {
        cout << "\nTarget cannot be placed on an obstacle!\n";
        return 0;
    }


    // =================================================
    // START AND TARGET SAME
    // =================================================

    if (samePosition(rover, target))
    {
        cout << "\nRover is already at the target!\n";
        return 0;
    }


    // =================================================
    // FIND SAFE PATH
    // =================================================

    cout << "\n=============================================\n";
    cout << "             CALCULATING PATH\n";
    cout << "=============================================\n";

    bool pathFound = findPath(
        rover,
        target,
        obstacles,
        path
    );


    // =================================================
    // NO PATH
    // =================================================

    if (!pathFound)
    {
        cout << "\nNo safe path exists to the target.\n";
        cout << "Rover cannot reach the destination.\n";

        return 0;
    }


    // =================================================
    // DISTANCE INFORMATION
    // =================================================

    int shortestDistance = path.size() - 1;

    int straightDistance =
        abs(target.x - rover.x) +
        abs(target.y - rover.y);


    cout << "\n=============================================\n";
    cout << "              PATH INFORMATION\n";
    cout << "=============================================\n";

    cout << "Starting position : ("
         << rover.x << ", "
         << rover.y << ")\n";

    cout << "Target position   : ("
         << target.x << ", "
         << target.y << ")\n";

    cout << "Direct distance   : "
         << straightDistance
         << " cells\n";

    cout << "Safe path distance: "
         << shortestDistance
         << " cells\n";

    cout << "=============================================\n";


    // =================================================
    // INITIAL STATE
    // =================================================

    RoverState state = MOVING;

    Direction direction = RIGHT;

    int step = 0;


    // Add starting point
    travelledPath.push_back(rover);


    // =================================================
    // DISPLAY INITIAL GRID
    // =================================================

    cout << "\nInitial Grid:\n";

    displayGrid(
        rover,
        target,
        direction,
        obstacles,
        travelledPath
    );


    this_thread::sleep_for(
        chrono::milliseconds(700)
    );


    // =================================================
    // MOVE ALONG SAFE PATH
    // =================================================

    for (int i = 1; i < path.size(); i++)
    {
        Position next = path[i];


        // =================================================
        // DETERMINE DIRECTION
        // =================================================

        Direction newDirection =
            getDirection(rover, next);


        // =================================================
        // CHECK WHETHER DIRECTION CHANGED
        // =================================================

        if (newDirection != direction)
        {
            state = AVOIDING;

            cout << "\n---------------------------------------------\n";

            cout << "Step: " << step << endl;

            cout << "Obstacle/path condition detected.\n";

            cout << "State: AVOIDING\n";

            cout << "Changing direction from ";

            showDirection(direction);

            cout << " to ";

            showDirection(newDirection);

            cout << endl;


            direction = newDirection;


            // Small delay for FSM visualization
            this_thread::sleep_for(
                chrono::milliseconds(500)
            );
        }


        // =================================================
        // MOVING STATE
        // =================================================

        state = MOVING;

        cout << "\nStep: " << step << endl;

        cout << "State: MOVING\n";

        cout << "Direction: ";

        showDirection(direction);

        cout << endl;


        // =================================================
        // MOVE ROVER
        // =================================================

        rover = next;

        travelledPath.push_back(rover);

        step++;


        cout << "Rover position: ("
             << rover.x << ", "
             << rover.y << ")\n";


        cout << "Distance travelled: "
             << step
             << " cells\n";


        cout << "Remaining distance: "
             << shortestDistance - step
             << " cells\n";


        // =================================================
        // CHECK TARGET
        // =================================================

        if (samePosition(rover, target))
        {
            state = REACHED;

            cout << "\n=============================================\n";
            cout << "             TARGET REACHED!\n";
            cout << "=============================================\n";

            cout << "Rover reached: ("
                 << rover.x << ", "
                 << rover.y << ")\n";

            cout << "Total distance travelled: "
                 << step
                 << " cells\n";

            cout << "State: REACHED\n";

            displayGrid(
                rover,
                target,
                direction,
                obstacles,
                travelledPath
            );

            break;
        }


        // =================================================
        // DISPLAY CURRENT GRID
        // =================================================

        displayGrid(
            rover,
            target,
            direction,
            obstacles,
            travelledPath
        );


        // =================================================
        // REAL-TIME DELAY
        // =================================================

        this_thread::sleep_for(
            chrono::milliseconds(300)
        );
    }


    // =================================================
    // FINAL STATE
    // =================================================

    if (state != REACHED)
    {
        state = STOPPED;
    }


    cout << "\n=============================================\n";
    cout << "              SIMULATION END\n";
    cout << "=============================================\n";

    cout << "Final position: ("
         << rover.x << ", "
         << rover.y << ")\n";

    cout << "Target position: ("
         << target.x << ", "
         << target.y << ")\n";

    cout << "Total steps: "
         << step
         << endl;

    cout << "Final state: ";

    if (state == REACHED)
    {
        cout << "REACHED";
    }
    else if (state == STOPPED)
    {
        cout << "STOPPED";
    }

    cout << endl;

    cout << "=============================================\n";


    return 0;
}
