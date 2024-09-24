package com.asist.asistmod.missionhelpers.mission;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

import net.minecraft.scoreboard.IScoreCriteria;
import net.minecraft.scoreboard.Score;
import net.minecraft.scoreboard.ScoreObjective;
import net.minecraft.scoreboard.ScorePlayerTeam;
import net.minecraft.scoreboard.ServerScoreboard;
import net.minecraft.server.MinecraftServer;

public class CustomScoreboard extends ServerScoreboard {
	
	/** Map of objective names to ScoreObjective objects. */
    private final Map<String, ScoreObjective> scoreObjectives = Maps.<String, ScoreObjective>newHashMap();
    /** Map of IScoreObjectiveCriteria objects to ScoreObjective objects. */
    private final Map<IScoreCriteria, List<ScoreObjective>> scoreObjectiveCriterias = Maps.<IScoreCriteria, List<ScoreObjective>>newHashMap();
    /** Map of entities name to ScoreObjective objects. */
    private final Map<String, Map<ScoreObjective, Score>> entitiesScoreObjectives = Maps.<String, Map<ScoreObjective, Score>>newHashMap();
    /** Index 0 is tab menu, 1 is sidebar, and 2 is below name */
    private final ScoreObjective[] objectiveDisplaySlots = new ScoreObjective[19];
    /** Map of teamnames to ScorePlayerTeam instances */
    private final Map<String, ScorePlayerTeam> teams = Maps.<String, ScorePlayerTeam>newHashMap();
    /** Map of usernames to ScorePlayerTeam objects. */
    private final Map<String, ScorePlayerTeam> teamMemberships = Maps.<String, ScorePlayerTeam>newHashMap();
    private static String[] displaySlots;

	public CustomScoreboard(MinecraftServer mcServer) {
		super(mcServer);
		// TODO Auto-generated constructor stub
	}
	
    @Override
    public Collection<Score> getSortedScores(ScoreObjective objective)
    {
        List<Score> list = Lists.<Score>newArrayList();

        for (Map<ScoreObjective, Score> map : this.entitiesScoreObjectives.values())
        {
            Score score = (Score)map.get(objective);

            if (score != null)
            {
                list.add(score);
            }
        }

        // Collections.sort(list, Score.SCORE_COMPARATOR);
        return list;
    }

}
