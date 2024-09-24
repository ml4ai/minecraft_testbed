package com.asist.asistmod.item;

import java.util.ArrayList;
import java.util.List;

import com.asist.asistmod.AsistMod;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.block.model.ModelResourceLocation;
import net.minecraft.item.Item;
import net.minecraft.item.Item.ToolMaterial;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.event.entity.player.PlayerSetSpawnEvent;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.registry.GameRegistry;
import net.minecraftforge.common.util.EnumHelper;

public class _Items {
	
	public static final List<Item> items = new ArrayList<Item>();
	
	
	public static Item itemFirstAid;
	public static Item itemUnpauseCookie;
	public static Item itemMarkingEraser;
	
	public static Item itemMedicalKit;
	public static Item itemStretcher;
	public static Item itemStretcherOccupied;
	public static Item itemHammer;
	
	public static Item itemMarkerRubble;
	public static Item itemMarkerVictim;
	public static Item itemMarkerClear;
	
	public static Item itemMarker1;
	public static Item itemMarker2;
	public static Item itemMarker3;
	public static Item itemMarker4;
	public static Item itemMarker5;
	public static Item itemMarker6;
	
	public static Item itemMarker1Red;
	public static Item itemMarker1Green;
	public static Item itemMarker1Blue;
	public static Item itemMarker2Red;
	public static Item itemMarker2Green;
	public static Item itemMarker2Blue;
	public static Item itemMarker3Red;
	public static Item itemMarker3Green;
	public static Item itemMarker3Blue;
	
	// 3.0 BELOW
	
	public static Item itemMarkerBlueAbrasion;
	public static Item itemMarkerBlueNoVictim;
	public static Item itemMarkerBlueSOS;
	public static Item itemMarkerBlueBoneDamage;
	public static Item itemMarkerBlueCritical;
	public static Item itemMarkerBlueCriticalVictim;
	public static Item itemMarkerBlueRegularVictim;
	public static Item itemMarkerBlueRubble;
	public static Item itemMarkerBlueThreat;
	public static Item itemMarkerBlueWildcard;
	
	public static Item itemMarkerGreenAbrasion;
	public static Item itemMarkerGreenNoVictim;
	public static Item itemMarkerGreenSOS;
	public static Item itemMarkerGreenBoneDamage;
	public static Item itemMarkerGreenCritical;
	public static Item itemMarkerGreenCriticalVictim;
	public static Item itemMarkerGreenRegularVictim;
	public static Item itemMarkerGreenRubble;
	public static Item itemMarkerGreenThreat;
	public static Item itemMarkerGreenWildcard;
	
	public static Item itemMarkerRedAbrasion;
	public static Item itemMarkerRedNoVictim;
	public static Item itemMarkerRedSOS;
	public static Item itemMarkerRedBoneDamage;
	public static Item itemMarkerRedCritical;
	public static Item itemMarkerRedCriticalVictim;
	public static Item itemMarkerRedRegularVictim;
	public static Item itemMarkerRedRubble;
	public static Item itemMarkerRedThreat;
	public static Item itemMarkerRedWildcard;
	
	
	
	//change to high durability
	public static final int medkitDurability = 5000;
	public static final int hammerDurability = 5000;
	public static final int stretcherDurability = 5000;
	
	// -1 to durability because you can use it once more at 0 durability
		public static final ToolMaterial medkitMaterial = 
				EnumHelper.addToolMaterial("custom_material", 0, medkitDurability-1, 1.0f, 0, 0);
		public static final ToolMaterial hammerMaterial = 
				EnumHelper.addToolMaterial("custom_material", 0, hammerDurability-1, 1.0f, 0, 0);
		public static final ToolMaterial stretcherMaterial = 
				EnumHelper.addToolMaterial("custom_material", 0, stretcherDurability-1, 0.0f, 0, 0);
	
	public static final void commonPreInit() {
		
		itemMedicalKit = registerItem(new MedicalKit("item_medical_kit", medkitMaterial), "item_medical_kit");
		itemHammer = registerItem(new Hammer("item_hammer", hammerMaterial), "item_hammer");
		itemStretcher = registerItem(new Stretcher("item_stretcher", stretcherMaterial), "item_stretcher");
		itemStretcherOccupied = registerItem(new Stretcher("item_stretcher_occupied", stretcherMaterial), "item_stretcher_occupied");

		
		itemFirstAid = registerItem(new Item(), "item_first_aid");
		itemUnpauseCookie = registerItem(new UnpauseCookie("item_unpause_cookie"), "item_unpause_cookie");
		itemMarkingEraser = registerItem(new Item(), "item_marking_eraser");
		
		itemMarkerRubble=registerItem(new Item(), "item_marker_rubble");
		itemMarkerVictim=registerItem(new Item(), "item_marker_victim");
		itemMarkerClear=registerItem(new Item(), "item_marker_clear");
		
		itemMarker1=registerItem(new Item(), "item_marker_1");
		itemMarker2=registerItem(new Item(), "item_marker_2");
		itemMarker3=registerItem(new Item(), "item_marker_3");
		itemMarker4=registerItem(new Item(), "item_marker_4");
		itemMarker5=registerItem(new Item(), "item_marker_5");
		itemMarker6=registerItem(new Item(), "item_marker_6");
		
		itemMarker1Red=registerItem(new Item(), "item_marker_1_red");
		itemMarker1Green=registerItem(new Item(), "item_marker_1_green");
		itemMarker1Blue=registerItem(new Item(), "item_marker_1_blue");
		itemMarker2Red=registerItem(new Item(), "item_marker_2_red");
		itemMarker2Green=registerItem(new Item(), "item_marker_2_green");
		itemMarker2Blue=registerItem(new Item(), "item_marker_2_blue");
		itemMarker3Red=registerItem(new Item(), "item_marker_3_red");
		itemMarker3Green=registerItem(new Item(), "item_marker_3_green");
		itemMarker3Blue=registerItem(new Item(), "item_marker_3_blue");
		
		// 3.0
		
		itemMarkerBlueAbrasion=registerItem(new Item(), "item_marker_blue_abrasion");
		itemMarkerBlueNoVictim=registerItem(new Item(), "item_marker_blue_novictim");
		itemMarkerBlueSOS=registerItem(new Item(), "item_marker_blue_sos");
		itemMarkerBlueBoneDamage=registerItem(new Item(), "item_marker_blue_bonedamage");
		itemMarkerBlueCritical=registerItem(new Item(), "item_marker_blue_critical");
		itemMarkerBlueCriticalVictim=registerItem(new Item(), "item_marker_blue_criticalvictim");
		itemMarkerBlueRegularVictim=registerItem(new Item(), "item_marker_blue_regularvictim");
		itemMarkerBlueRubble=registerItem(new Item(), "item_marker_blue_rubble");
		itemMarkerBlueThreat=registerItem(new Item(), "item_marker_blue_threat");
		itemMarkerBlueWildcard=registerItem(new Item(), "item_marker_blue_wildcard");
		
		itemMarkerGreenAbrasion=registerItem(new Item(), "item_marker_green_abrasion");
		itemMarkerGreenNoVictim=registerItem(new Item(), "item_marker_green_novictim");
		itemMarkerGreenSOS=registerItem(new Item(), "item_marker_green_sos");
		itemMarkerGreenBoneDamage=registerItem(new Item(), "item_marker_green_bonedamage");
		itemMarkerGreenCritical=registerItem(new Item(), "item_marker_green_critical");
		itemMarkerGreenCriticalVictim=registerItem(new Item(), "item_marker_green_criticalvictim");
		itemMarkerGreenRegularVictim=registerItem(new Item(), "item_marker_green_regularvictim");
		itemMarkerGreenRubble=registerItem(new Item(), "item_marker_green_rubble");
		itemMarkerGreenThreat=registerItem(new Item(), "item_marker_green_threat");
		itemMarkerGreenWildcard=registerItem(new Item(), "item_marker_green_wildcard");
		
		itemMarkerRedAbrasion=registerItem(new Item(), "item_marker_red_abrasion");
		itemMarkerRedNoVictim=registerItem(new Item(), "item_marker_red_novictim");
		itemMarkerRedSOS=registerItem(new Item(), "item_marker_red_sos");
		itemMarkerRedBoneDamage=registerItem(new Item(), "item_marker_red_bonedamage");
		itemMarkerRedCritical=registerItem(new Item(), "item_marker_red_critical");
		itemMarkerRedCriticalVictim=registerItem(new Item(), "item_marker_red_criticalvictim");
		itemMarkerRedRegularVictim=registerItem(new Item(), "item_marker_red_regularvictim");
		itemMarkerRedRubble=registerItem(new Item(), "item_marker_red_rubble");
		itemMarkerRedThreat=registerItem(new Item(), "item_marker_red_threat");
		itemMarkerRedWildcard=registerItem(new Item(), "item_marker_red_wildcard");
		
		items.add(itemMedicalKit);
		items.add(itemHammer);
		items.add(itemStretcher);
		items.add(itemStretcherOccupied);
		
	
		items.add(itemFirstAid);
		items.add(itemUnpauseCookie);
		items.add(itemMarkingEraser);
		
		items.add(itemMarkerRubble);
		items.add(itemMarkerVictim);
		items.add(itemMarkerClear);
		
		items.add(itemMarker1);
		items.add(itemMarker2);
		items.add(itemMarker3);
		items.add(itemMarker4);
		items.add(itemMarker5);
		items.add(itemMarker6);
		
		items.add(itemMarker1Red);
		items.add(itemMarker1Green);
		items.add(itemMarker1Blue);
		items.add(itemMarker2Red);
		items.add(itemMarker2Green);
		items.add(itemMarker2Blue);
		items.add(itemMarker3Red);
		items.add(itemMarker3Green);
		items.add(itemMarker3Blue);
		
		items.add(itemMarkerBlueAbrasion);
		items.add(itemMarkerBlueBoneDamage);
		items.add(itemMarkerBlueCritical);
		items.add(itemMarkerBlueCriticalVictim);
		items.add(itemMarkerBlueRegularVictim);
		items.add(itemMarkerBlueNoVictim);
		items.add(itemMarkerBlueRubble);
		items.add(itemMarkerBlueThreat);
		items.add(itemMarkerBlueWildcard);
		
		items.add(itemMarkerGreenAbrasion);
		items.add(itemMarkerGreenBoneDamage);
		items.add(itemMarkerGreenNoVictim);
		items.add(itemMarkerGreenCritical);
		items.add(itemMarkerGreenCriticalVictim);
		items.add(itemMarkerGreenRegularVictim);
		items.add(itemMarkerGreenRubble);
		items.add(itemMarkerGreenThreat);
		items.add(itemMarkerGreenWildcard);
		
		items.add(itemMarkerRedAbrasion);
		items.add(itemMarkerRedBoneDamage);
		items.add(itemMarkerRedNoVictim);
		items.add(itemMarkerRedCritical);
		items.add(itemMarkerRedCriticalVictim);
		items.add(itemMarkerRedRegularVictim);
		items.add(itemMarkerRedRubble);
		items.add(itemMarkerRedThreat);
		items.add(itemMarkerRedWildcard);
	}
	
	public static final void clientPostInit() {
		for(Item item : items) {
			registerRender(item);
		}	
	}
	
	private static final void registerRender(Item item) {
		Minecraft.getMinecraft().getRenderItem().getItemModelMesher().register(item, 0, new ModelResourceLocation(AsistMod.MODID + ":" + item.getRegistryName().getResourcePath(), "inventory"));
	}
	
	public static final Item registerItem(Item item, String name) {
		item.setUnlocalizedName(name);
		GameRegistry.register(item, new ResourceLocation(AsistMod.MODID, name));		
		items.add(item);
		return item;
	}
}
