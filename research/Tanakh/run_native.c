#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

extern void tanakh_transform(void);
extern uint64_t state, relations, constraints, observations;
extern uint64_t unresolved, context, target, events;

int main(void) {
    tanakh_transform();
    printf("{\"state\":%" PRIu64 ",\"relations\":%" PRIu64
           ",\"constraints\":%" PRIu64 ",\"observations\":%" PRIu64
           ",\"unresolved\":%" PRIu64 ",\"context\":%" PRIu64
           ",\"target\":%" PRIu64 ",\"events\":%" PRIu64 "}\n",
           state, relations, constraints, observations,
           unresolved, context, target, events);
    return 0;
}
