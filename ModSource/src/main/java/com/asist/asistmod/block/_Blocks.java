package com.asist.asistmod.block;

import java.util.HashMap;

import com.asist.asistmod.AsistMod;
import com.asist.asistmod.item._Items;
import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.item.Item;
import net.minecraft.item.ItemBlock;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.fml.common.registry.GameRegistry;

public class _Blocks {
	
	public static final HashMap<Block,Item> blocks = new HashMap<Block,Item>();
	
	private static Block blockVictim_1;
	private static Block blockVictim_1b;
	private static Block blockVictim_2;
	
	private static Block blockVictim_saved_a;
	private static Block blockVictim_saved_b;
	private static Block blockVictim_saved_c;
	
	//private static Block blockVictim_3;
	
	private static Block blockVictim_proximity;
	
	private static Block blockVictim_1_marking;
	private static Block blockVictim_2_marking;
	
	private static Block blockVictim_saved;
	private static Block blockVictim_expired;
	
	private static Block blockIntervention_backward;
	private static Block blockIntervention_forward;
	private static Block blockIntervention_left;
	private static Block blockIntervention_right;
	private static Block blockIntervention_no_victims;
	private static Block blockIntervention_path_clear;
	private static Block blockIntervention_path_blocked;
	private static Block blockIntervention_unexplored;
	
	private static Block blockFreezePlayer;

	private static Block blockRubbleCollapse;

	private static Block blockRole_swap_admin;
	private static Block blockRole_swap_med;
	private static Block blockRole_swap_hms;
	private static Block blockRole_swap_ss;
	
	private static Block blockPerturbation_victim;
	private static Block blockPerturbation_gasleak;
	
	private static Block blockMission_1;
	private static Block blockMission_2;
	
	public static CustomCarpetBlock blockMarkerBlueAbrasion;
	public static CustomCarpetBlock blockMarkerBlueNoVictim;
	public static CustomCarpetBlock blockMarkerBlueSOS;
	public static CustomCarpetBlock blockMarkerBlueBoneDamage;
	public static CustomCarpetBlock blockMarkerBlueCritical;
	public static CustomCarpetBlock blockMarkerBlueCriticalVictim;
	public static CustomCarpetBlock blockMarkerBlueRegularVictim;
	public static CustomCarpetBlock blockMarkerBlueRubble;
	public static CustomCarpetBlock blockMarkerBlueThreat;
	public static CustomCarpetBlock blockMarkerBlueWildcard;
	
	public static CustomCarpetBlock blockMarkerGreenAbrasion;
	public static CustomCarpetBlock blockMarkerGreenNoVictim;
	public static CustomCarpetBlock blockMarkerGreenSOS;
	public static CustomCarpetBlock blockMarkerGreenBoneDamage;
	public static CustomCarpetBlock blockMarkerGreenCritical;
	public static CustomCarpetBlock blockMarkerGreenCriticalVictim;
	public static CustomCarpetBlock blockMarkerGreenRegularVictim;
	public static CustomCarpetBlock blockMarkerGreenRubble;
	public static CustomCarpetBlock blockMarkerGreenThreat;
	public static CustomCarpetBlock blockMarkerGreenWildcard;
	
	public static CustomCarpetBlock blockMarkerRedAbrasion;
	public static CustomCarpetBlock blockMarkerRedNoVictim;
	public static CustomCarpetBlock blockMarkerRedSOS;
	public static CustomCarpetBlock blockMarkerRedBoneDamage;
	public static CustomCarpetBlock blockMarkerRedCritical;
	public static CustomCarpetBlock blockMarkerRedCriticalVictim;
	public static CustomCarpetBlock blockMarkerRedRegularVictim;
	public static CustomCarpetBlock blockMarkerRedRubble;
	public static CustomCarpetBlock blockMarkerRedThreat;
	public static CustomCarpetBlock blockMarkerRedWildcard;
	
	public static BlockSignalVictim blockSignalVictim;
	
	private static Block blockRole_swap_eng;
	private static Block blockRole_swap_medic;
	private static Block blockRole_swap_trans;
	
	// dont foreget new role blocks
	
	public static final void commonPreInit() {
		
		// Victim Blocks
		
		blockVictim_1 = registerBlock(new BlockVictim_1(),"block_victim_1");
		blockVictim_1b = registerBlock(new BlockVictim_1b(),"block_victim_1b");
		blockVictim_2 = registerBlock(new BlockVictim_2(),"block_victim_2");
		//blockVictim_3 = registerBlock(new BlockVictim_3(),"block_victim_3");
		
		blockVictim_proximity = registerBlock(new BlockVictim_Proximity(), "block_victim_proximity");
		blockFreezePlayer = registerBlock(new BlockFreezePlayer(Material.GOURD),"block_freeze_player");

		blockRubbleCollapse = registerBlock(new BlockRubble_Collapse(Material.GOURD),"block_rubble_collapse");

		blockVictim_1_marking = registerBlock(new BlockVictim_1_Marking(),"block_victim_1_marking");
		blockVictim_2_marking = registerBlock(new BlockVictim_2_Marking(),"block_victim_2_marking");
		
		blockVictim_saved = registerBlock(new BlockVictim_Saved(),"block_victim_saved");
		
		
		// THE GAME REGISTERS 3 BLOCKS THAT ARE EXACTLY THE SAME, BUT WITH DIFFERENT REGISTRY NAMES
		blockVictim_saved_a = registerBlock(new BlockVictim_Saved(),"block_victim_saved_a");
		blockVictim_saved_b = registerBlock(new BlockVictim_Saved(),"block_victim_saved_b");
		blockVictim_saved_c = registerBlock(new BlockVictim_Saved(),"block_victim_saved_c");
		
		
		blockVictim_expired = registerBlock(new BlockVictim_Expired(),"block_victim_expired");
		
		blockRole_swap_admin = registerBlock(new BlockRole_Admin(), "block_role_admin");
		blockRole_swap_med = registerBlock(new BlockRole_Med(), "block_role_med");
		blockRole_swap_hms = registerBlock(new BlockRole_HS(), "block_role_hs");
		blockRole_swap_ss = registerBlock(new BlockRole_SS(), "block_role_ss");
		
		blockPerturbation_victim = registerBlock(new BlockPerturbation_Victim(), "block_perturbation_victim");
		blockPerturbation_gasleak = registerBlock(new BlockPerturbation_Gasleak(), "block_perturbation_gasleak");

		blockMission_1 = registerBlock(new BlockMission_Tutorial(),"block_mission_tutorial");
		blockMission_2 = registerBlock(new BlockMission_Mission(),"block_mission_mission");
		
		// Intervention Blocks
		
		blockIntervention_backward = registerBlock(new Block(Material.GOURD),"block_intervention_backward");
		blockIntervention_forward = registerBlock(new Block(Material.GOURD),"block_intervention_forward");
		blockIntervention_left = registerBlock(new Block(Material.GOURD),"block_intervention_left");
		blockIntervention_right = registerBlock(new Block(Material.GOURD),"block_intervention_right");
		blockIntervention_no_victims = registerBlock(new Block(Material.GOURD),"block_intervention_no_victims");
		blockIntervention_path_clear = registerBlock(new Block(Material.GOURD),"block_intervention_path_clear");
		blockIntervention_path_blocked = registerBlock(new Block(Material.GOURD),"block_intervention_path_blocked");
		blockIntervention_unexplored = registerBlock(new Block(Material.GOURD),"block_intervention_unexplored");
	
		// this is here just so the carpet blocks can be scrutinized closely, but should really be moved to		
		// register block function
		
		try {
			
			CustomCarpetBlock carpetBlockVictim = new CustomCarpetBlock("victim");
			CustomCarpetBlock carpetBlockRubble = new CustomCarpetBlock("rubble");
			CustomCarpetBlock carpetBlockClear = new CustomCarpetBlock("clear");
			
			carpetBlockVictim.setUnlocalizedName("block_marker_victim");
			GameRegistry.register(carpetBlockVictim, new ResourceLocation(AsistMod.MODID, "block_marker_victim"));	
			_Items.registerItem(new ItemBlock(carpetBlockVictim), "block_marker_victim");
			
			carpetBlockRubble.setUnlocalizedName("block_marker_rubble");
			GameRegistry.register(carpetBlockRubble, new ResourceLocation(AsistMod.MODID, "block_marker_rubble"));	
			_Items.registerItem(new ItemBlock(carpetBlockRubble), "block_marker_rubble");
			
			carpetBlockClear.setUnlocalizedName("block_marker_clear");
			GameRegistry.register(carpetBlockClear, new ResourceLocation(AsistMod.MODID, "block_marker_clear"));	
			_Items.registerItem(new ItemBlock(carpetBlockClear), "block_marker_clear");
			
			CustomCarpetBlock carpetBlock1Red = new CustomCarpetBlock("1Red");
			CustomCarpetBlock carpetBlock1Green = new CustomCarpetBlock("1Green");
			CustomCarpetBlock carpetBlock1Blue = new CustomCarpetBlock("1Blue");
			CustomCarpetBlock carpetBlock2Red = new CustomCarpetBlock("2Red");
			CustomCarpetBlock carpetBlock2Green = new CustomCarpetBlock("2Green");
			CustomCarpetBlock carpetBlock2Blue = new CustomCarpetBlock("2Blue");
			CustomCarpetBlock carpetBlock3Red = new CustomCarpetBlock("3Red");
			CustomCarpetBlock carpetBlock3Green = new CustomCarpetBlock("3Green");
			CustomCarpetBlock carpetBlock3Blue = new CustomCarpetBlock("3Blue");

			
			registerBlock(carpetBlock1Red,"block_marker_1_red");
			registerBlock(carpetBlock1Green,"block_marker_1_green");
			registerBlock(carpetBlock1Blue,"block_marker_1_blue");
			registerBlock(carpetBlock2Red,"block_marker_2_red");
			registerBlock(carpetBlock2Green,"block_marker_2_green");
			registerBlock(carpetBlock2Blue,"block_marker_2_blue");
			registerBlock(carpetBlock3Red,"block_marker_3_red");
			registerBlock(carpetBlock3Green,"block_marker_3_green");
			registerBlock(carpetBlock3Blue,"block_marker_3_blue");
			
	
			
			
		}
		catch(Exception e) {
			
			e.printStackTrace();
			
		}
		
		blockMarkerBlueAbrasion=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_abrasion");
		blockMarkerBlueNoVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_novictim");
		blockMarkerBlueSOS=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_sos");
		blockMarkerBlueBoneDamage=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_bonedamage");
		blockMarkerBlueCritical=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_critical");
		blockMarkerBlueCriticalVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_criticalvictim");
		blockMarkerBlueRegularVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_regularvictim");
		blockMarkerBlueRubble=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_rubble");
		blockMarkerBlueThreat=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_threat");
		blockMarkerBlueWildcard=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_blue_wildcard");
		
		blockMarkerGreenAbrasion=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_abrasion");
		blockMarkerGreenNoVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_novictim");
		blockMarkerGreenSOS=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_sos");
		blockMarkerGreenBoneDamage=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_bonedamage");
		blockMarkerGreenCritical=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_critical");
		blockMarkerGreenCriticalVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_criticalvictim");
		blockMarkerGreenRegularVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_regularvictim");
		blockMarkerGreenRubble=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_rubble");
		blockMarkerGreenThreat=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_threat");
		blockMarkerGreenWildcard=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_green_wildcard");
		
		blockMarkerRedAbrasion=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_abrasion");
		blockMarkerRedNoVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_novictim");
		blockMarkerRedSOS=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_sos");
		blockMarkerRedBoneDamage=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_bonedamage");
		blockMarkerRedCritical=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_critical");
		blockMarkerRedCriticalVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_criticalvictim");
		blockMarkerRedRegularVictim=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_regularvictim");
		blockMarkerRedRubble=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_rubble");
		blockMarkerRedThreat=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_threat");
		blockMarkerRedWildcard=(CustomCarpetBlock)registerBlock(new CustomCarpetBlock(null), "block_marker_red_wildcard");

		blockRole_swap_medic = registerBlock(new BlockRole_Med(), "block_role_medic");
		blockRole_swap_eng = registerBlock(new BlockRole_HS(), "block_role_engineer");
		blockRole_swap_trans = registerBlock(new BlockRole_SS(), "block_role_transporter");
		
		blockSignalVictim = (BlockSignalVictim)registerBlock(new BlockSignalVictim(Material.GOURD), "block_signal_victim");
		
	}
	
	public static final Block registerBlock(Block block, String name) {
		
		block.setUnlocalizedName(name);
		GameRegistry.register(block, new ResourceLocation(AsistMod.MODID, name));		
		Item blockItem = _Items.registerItem(new ItemBlock(block), name);
		blocks.put(block, blockItem);
		return block;
		
	}

}
