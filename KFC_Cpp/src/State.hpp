#pragma once

#include "Moves.hpp"
#include "Graphics.hpp"
#include "Physics.hpp"
#include <unordered_map>
#include <memory>
#include <string>

class State {
public:
    State(std::shared_ptr<Moves> moves,
          std::shared_ptr<Graphics> graphics,
          std::shared_ptr<BasePhysics> physics)
        : moves(std::move(moves)), graphics(std::move(graphics)), physics(std::move(physics)) {}

    std::shared_ptr<Moves>    moves;
    std::shared_ptr<Graphics> graphics;
    std::shared_ptr<BasePhysics> physics;

    std::unordered_map<std::string, State*> transitions;
    std::string name;

    void set_transition(const std::string& event, State* target) { transitions[event] = target; }

    void reset(const Command& cmd) {
        graphics->reset(cmd);
        physics->reset(cmd);
    }

    State* on_command(const Command& cmd) {
        std::string key = cmd.type;
        for(auto& ch : key) ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
        auto it = transitions.find(key);
        if(it != transitions.end()) {
            State* next = it->second;
            next->reset(cmd);
            return next;
        }
        return this;
    }

    State* update(int now_ms) {
        auto internal = physics->update(now_ms);
        if(internal) {
            return on_command(*internal);
        }
        return this;
    }

    bool can_be_captured() const { return physics->can_be_captured(); }
    bool can_capture()    const { return physics->can_capture(); }
}; 