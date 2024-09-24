package com.asist.asistmod.missionhelpers.rubble_collapse;

import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.datamodels.PositionRange.PositionRangeModel;
import com.asist.asistmod.missionhelpers.datastructures.PositionRange;

import net.minecraft.util.math.BlockPos;

public class RubbleCollapseManager {
	
	public static ConcurrentHashMap<BlockPos,PositionRangeModel> collapseMap = new ConcurrentHashMap<BlockPos,PositionRangeModel>();
	public static ConcurrentHashMap<BlockPos,Long> collapseTimerMap = new ConcurrentHashMap<BlockPos,Long>();

	public RubbleCollapseManager() {
		// TODO Auto-generated constructor stub
	}
	
	
	public static PositionRangeModel getBlock(BlockPos bp) {
		
		PositionRangeModel prm = null;
		try{
			prm = collapseMap.get(bp);
		}catch(Exception e) {
			
			System.out.println("Error @ CollapseMap! There was no collapse block with this position!");
			System.out.println(e.getStackTrace());
		}
		
		return prm;
	}
	
	public static void createCollapseLink(BlockPos bp, PositionRangeModel pr) {
		collapseMap.put(bp, pr);
		
	}
	
	public static void setCollapseTime(BlockPos bp, Long l) {
		collapseTimerMap.put(bp, l);
	}
	
	public static long getLastCollapseTime(BlockPos bp) {
		
		// so big it will never be greater than 5 seconds with the math we use
		long l = 5000000;
		try{
			l = collapseTimerMap.get(bp);
		}catch(Exception e) {
			
			System.out.println("Error @ CollapseTimerMap! There was no collapse block with this position!");
			System.out.println(e.getStackTrace());
		}
		
		return l;
	}
	
	public static String printCollapseMap() {
		StringBuilder sb = new StringBuilder("");
		
		collapseMap.forEach((k,v) -> {
			sb.append(k);
			sb.append( " : ");
			sb.append( v.getString() );
			sb.append( "\n" );
		});
		
		return sb.toString();
	}

}
