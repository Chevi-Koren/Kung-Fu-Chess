#include <doctest/doctest.h>

#include "../src/Physics.hpp"
#include "../src/State.hpp"
#include "../src/Piece.hpp"
#include "../src/Board.hpp"
#include "../src/Graphics.hpp"
#include "../src/img.hpp"

#include <vector>
#include <cmath>

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
static Board make_board(int cells=8, int px=1) {
    Img blank; // no real image – headless
    return Board(px, px, cells, cells, blank);
}

static std::shared_ptr<Graphics> dummy_gfx() {
    return std::make_shared<Graphics>("", std::pair<int,int>{1,1});
}

// ---------------------------------------------------------------------------
TEST_CASE("MovePhysics full cycle") {
    Board board = make_board();

    MovePhysics phys(board, 1.0); // 1 cell per second
    Command cmd(0, "P", "move", {{0,0},{0,2}});
    phys.reset(cmd);

    // halfway (1 s) – still moving
    CHECK(phys.update(1000) == std::nullopt);

    // Slightly beyond expected duration (2.1s) – should emit done
    auto done = phys.update(2100);
    REQUIRE(done);
    CHECK(done->type == "done");
    CHECK(phys.get_curr_cell() == std::pair<int,int>{0,2});
}

TEST_CASE("JumpPhysics & RestPhysics duration") {
    Board board = make_board();

    JumpPhysics jump(board, 0.05); // 50 ms
    Command start(0, "J", "jump", {{1,1}});
    jump.reset(start);
    CHECK(jump.update(20) == std::nullopt);
    CHECK(jump.update(100)->type == "done");

    RestPhysics rest(board, 0.05);
    rest.reset(start);
    CHECK(rest.update(20) == std::nullopt);
    CHECK(rest.update(100)->type == "done");
}

TEST_CASE("State transition idle→move→idle via internal done") {
    Board board = make_board();

    // Build graphics once
    auto gfx = dummy_gfx();

    // Physics per state
    auto idle_phys = std::make_shared<IdlePhysics>(board);
    auto move_phys = std::make_shared<MovePhysics>(board, 1.0);

    // States
    auto idle = std::make_shared<State>(nullptr, gfx, idle_phys);
    idle->name = "idle";
    auto move = std::make_shared<State>(nullptr, gfx, move_phys);
    move->name = "move";

    idle->set_transition("move", move);
    move->set_transition("done", idle);

    Piece piece("PX", idle);

    Command mv(0, piece.id, "move", {{0,0},{0,1}});
    piece.on_command(mv, Piece::Cell2Pieces{});
    CHECK(piece.state == move);

    // advance 2s so move ends
    piece.update(2100);
    CHECK(piece.state == idle);
} 

TEST_CASE("IdlePhysics properties") {
    Board board = make_board();

    IdlePhysics phys(board);
    Command cmd(0, "P", "idle", {{2,3}});
    phys.reset(cmd);

    CHECK(phys.get_curr_cell() == std::pair<int,int>{2,3});
    CHECK(phys.update(100) == std::nullopt);
    CHECK(!phys.can_capture());
    CHECK(phys.is_movement_blocker());
}

TEST_CASE("Jump & Rest physics special flags") {
    Board board = make_board();

    JumpPhysics jump(board, 0.05);
    RestPhysics rest(board, 0.05);
    Command start(0, "J", "jump", {{1,1}});

    jump.reset(start);
    rest.reset(start);

    CHECK(!jump.can_be_captured());  // invulnerable while jumping
    CHECK(!rest.can_capture());      // resting pieces cannot capture
    CHECK(rest.is_movement_blocker());
} 