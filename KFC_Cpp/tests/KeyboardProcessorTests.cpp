#include <doctest/doctest.h>

#include "../src/KeyboardProcessor.hpp"

#include <thread>
#include <vector>
#include <string>
#include <unordered_map>
#include <chrono>

static std::string make_event(const std::string& key) {
    return key; // direct pass
}

TEST_CASE("KeyboardProcessor initial position and get_cursor") {
    std::unordered_map<std::string,std::string> keymap{{"w","up"},{"s","down"},{"a","left"},{"d","right"},{"enter","choose"},{"+","jump"}};
    KeyboardProcessor kp(8,8,keymap);
    CHECK(kp.get_cursor() == std::pair<int,int>{0,0});
}

TEST_CASE("KeyboardProcessor cursor moves and wraps") {
    std::unordered_map<std::string,std::string> km{{"w","up"},{"s","down"},{"a","left"},{"d","right"}};
    KeyboardProcessor kp(2,3,km);

    kp.process_key(make_event("w")); // up stays
    CHECK(kp.get_cursor() == std::pair<int,int>{0,0});
    kp.process_key("s");
    CHECK(kp.get_cursor() == std::pair<int,int>{1,0});
    kp.process_key("s");
    CHECK(kp.get_cursor() == std::pair<int,int>{1,0});
    kp.process_key("a");
    CHECK(kp.get_cursor() == std::pair<int,int>{1,0});
    kp.process_key("d");
    CHECK(kp.get_cursor() == std::pair<int,int>{1,1});
}

TEST_CASE("KeyboardProcessor choose and jump return actions") {
    std::unordered_map<std::string,std::string> km{{"w","up"},{"s","down"},{"a","left"},{"d","right"},{"enter","choose"},{"+","jump"}};
    KeyboardProcessor kp(5,5,km);
    kp.process_key("enter");
    CHECK(kp.process_key("enter") == "choose");
    CHECK(kp.process_key("+") == "jump");
    CHECK(kp.process_key("w") == "up");
    CHECK(kp.process_key("x").empty());
}

void worker_thread(KeyboardProcessor* kp, const std::vector<std::string>& keys) {
    for(const auto& k : keys) {
        kp->process_key(k);
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}

TEST_CASE("KeyboardProcessor thread safety") {
    std::unordered_map<std::string,std::string> km{{"up","up"},{"down","down"},{"left","left"},{"right","right"}};
    KeyboardProcessor kp(8,8,km);
    std::vector<std::string> seq1 = {"up","up","left","down","right"};
    std::vector<std::string> seq2 = {"down","right","right","up","left"};
    seq1.resize(2500);
    seq2.resize(2500);
    // fill pattern repeated
    for(size_t i=5;i<2500;++i){seq1[i]=seq1[i-5]; seq2[i]=seq2[i-5];}
    std::thread t1(worker_thread,&kp,seq1);
    std::thread t2(worker_thread,&kp,seq2);
    t1.join(); t2.join();

    auto cur = kp.get_cursor();
    CHECK(cur.first >=0 && cur.first < 8);
    CHECK(cur.second >=0 && cur.second < 8);
} 