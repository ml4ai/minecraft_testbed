package com.asist.asistmod.missionhelpers.enums;

import net.minecraft.block.state.IBlockState;
import net.minecraft.init.Blocks;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public enum BlockType {
	VICTIM_A		("victim_a", "victim_a","asistmod:block_victim_1", 
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_1")).getDefaultState()),
	VICTIM_C		("victim_c", "victim_c","asistmod:block_victim_2",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_2")).getDefaultState()),
	VICTIM_B		("victim_b", "victim_b","asistmod:block_victim_1b",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_1b")).getDefaultState()),
	VICTIM_SAVED	("victim_saved", "saved","asistmod:block_victim_saved",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_saved")).getDefaultState()),
	VICTIM_SAVED_A	("victim_saved_a", "saved","asistmod:block_victim_saved_a",
			ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_saved_a")).getDefaultState()),
	VICTIM_SAVED_B	("victim_saved_b", "saved","asistmod:block_victim_saved_b",
			ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_saved_b")).getDefaultState()),
	VICTIM_SAVED_C	("victim_saved_c", "saved","asistmod:block_victim_saved_c",
			ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_victim_saved_c")).getDefaultState()),	
	ROLE_ADMIN		("role_admin", "admin","asistmod:block_role_admin",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_role_admin")).getDefaultState()),
	ROLE_ENG		("role_eng", "hammer","asistmod:block_role_engineer",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_role_engineer")).getDefaultState()),
	ROLE_MED		("role_med", "medical","asistmod:block_role_medical",
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_role_medic")).getDefaultState()),
	ROLE_TRAN			("role_tran", "search","asistmod:block_role_transporter", 
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_role_transporter")).getDefaultState()),
	TUTORIAL		("mission_tutorial", "tutorial","asistmod:block_mission_tutorial", 
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_mission_tutorial")).getDefaultState()),
	MISSION			("mission_mission", "mission","asistmod:block_mission_mission", 
						ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", "block_mission_mission")).getDefaultState()),
	NULL			("air", "air","minecraft:air", Blocks.AIR.getDefaultState());
		
	private final String name;
	private final String typeName;
	private final IBlockState blockState;
	private final String registryName;
	
	BlockType(String name, String typeName, String registryName, IBlockState blockState) {
		this.name = name;
		this.typeName = typeName;
		this.blockState = blockState;
		this.registryName = registryName;
	}
		
	public String getName() {
		return this.name;
	}
	
	public String getTypeName() {
		return this.typeName;
	}
	
	public String getRegistryName() {
		return this.registryName;
	}
		
	public IBlockState getDefaultState() {
		return this.blockState;
	}
}
