package com.asist.asistmod.missionhelpers.mod;

import com.asist.asistmod.missionhelpers.enums.BlockType;
import com.asist.asistmod.missionhelpers.enums.RoleType;

import net.minecraft.block.state.IBlockState;

public class ModBlocks {
	
	static BlockType stretcherBlocks[] = {	
						BlockType.VICTIM_A,	
						BlockType.VICTIM_B,
						//BlockType.VICTIM_C,
						BlockType.VICTIM_SAVED_A,
						BlockType.VICTIM_SAVED_B,
						BlockType.VICTIM_SAVED_C
						
						};
	
	static BlockType victimBlocks[] = {
						BlockType.VICTIM_A,	
						BlockType.VICTIM_B,
						BlockType.VICTIM_C,
						BlockType.VICTIM_SAVED_A,
						BlockType.VICTIM_SAVED_B,
						BlockType.VICTIM_SAVED_C
						};
	
	static BlockType roleBlocks[] = {		
						BlockType.ROLE_ADMIN,
						BlockType.ROLE_TRAN,
						BlockType.ROLE_MED,
						BlockType.ROLE_ENG,
						};
	
	static BlockType missionBlocks[] = {	
						BlockType.TUTORIAL,
						BlockType.MISSION,
						};
	

	public static BlockType getEnum(IBlockState block) {
		for(BlockType type : BlockType.values()) {
			if(block == type.getDefaultState()) { return type; }
		}
		return BlockType.NULL;
	}
	
	public static RoleType getRole(BlockType blockType) {
		for(RoleType type : RoleType.values()) {
			if(blockType.getTypeName() == type.getName()) { return type; }
		}
		return RoleType.NULL;
	}
	
	public static BlockType getEnum(String blockName) {
		for(BlockType type : BlockType.values()) {
			if(blockName == type.getName()) { return type; }
		}
		return BlockType.NULL;
	}
	
	public static BlockType getEnumFromRegistryName(String registryName) {
		for(BlockType type : BlockType.values()) {
			if( registryName.contentEquals( type.getRegistryName() ) ) { return type; }
		}
		return BlockType.NULL;
	}
	
	public static boolean isBlock(IBlockState block, BlockType modBlock) {
		return block == modBlock.getDefaultState() ? true : false;
	}
	
	public static boolean canPickUp(BlockType modBlock) {
		for(BlockType type: stretcherBlocks) {
			if(modBlock.equals(type)) { return true; }
		}
		return false;
	}
	
	public static boolean isRoleBlock(BlockType modBlock) {
		for(BlockType type: roleBlocks) {
			if(modBlock.equals(type)) { return true; }
		}
		return false;
	}
	
	public static boolean isMissionBlock(BlockType modBlock) {
		for(BlockType type: missionBlocks) {
			if(modBlock.equals(type)) { return true; }
		}
		return false;
	}
	
	public static boolean isVictimBlock(BlockType modBlock) {
		for(BlockType type: victimBlocks) {
			if(modBlock.equals(type)) { return true; }
		}
		return false;
	}
}
