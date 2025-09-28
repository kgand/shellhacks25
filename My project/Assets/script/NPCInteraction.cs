using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

[System.Serializable]
public class TransitionRule
{
    [Tooltip("如果玩家分数 '小于等于' 此值，则跳转到指定场景")]
    public int scoreThreshold;
    public string sceneName;
}

public class NPCInteraction : MonoBehaviour
{
    [Header("叙事内容")]
    [TextArea(3, 10)] // Increased the size for longer text
    public string narrationLine;
    // We no longer need delayBeforeChoices, the system is now dynamic.

    [Header("选择内容")]
    public string choicePrompt;
    public List<Choice> choices;

    [Header("场景跳转规则")]
    [Tooltip("请按分数阈值从低到高排序。如果没有满足的规则，将不会跳转。")]
    public List<TransitionRule> transitionRules;

    [Header("必要组件引用")]
    [Tooltip("请将场景中的ChoicePanel拖拽到这里")]
    public ChoicePanelController choicePanel;

    private bool hasBeenTriggered = false;

    void Start()
    {
        if (choicePanel == null)
        {
            Debug.LogError("NPCInteraction 脚本没有指定 ChoicePanelController 的引用！请在Inspector中拖拽赋值。", this.gameObject);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player") && !hasBeenTriggered)
        {
            hasBeenTriggered = true;
            StartCoroutine(InteractionSequence());
        }
    }

    private IEnumerator InteractionSequence()
    {
        // 1. Show the narration and start the typewriter effect
        StoryManager.Instance.ShowNarration(narrationLine);

        // 2. IMPORTANT: Wait until the typewriter effect is completely finished
        yield return new WaitUntil(() => !StoryManager.Instance.narrationController.isTyping);
        
        // Add a small dramatic pause after typing finishes
        yield return new WaitForSeconds(0.5f);

        // 3. Hide the narration panel now that it has been read
        StoryManager.Instance.narrationController.Hide();

        // 4. Show the choice panel
        choicePanel.SetupAndShow(choicePrompt, choices);
        GetComponent<Collider>().enabled = false;

        // 5. Wait until the player makes a choice (panel is hidden)
        yield return new WaitUntil(() => !choicePanel.gameObject.activeInHierarchy);
        
        // 6. Process the scene transition based on the choice
        ProcessSceneTransition();
    }
    
    private void ProcessSceneTransition()
    {
        if (transitionRules == null || transitionRules.Count == 0)
        {
            Debug.Log("没有设置场景跳转规则，停留在当前场景。");
            return;
        }

        int currentScore = StoryManager.Instance.memoryClarityScore;
        List<TransitionRule> sortedRules = transitionRules.OrderBy(rule => rule.scoreThreshold).ToList();

        foreach (var rule in sortedRules)
        {
            if (currentScore <= rule.scoreThreshold)
            {
                Debug.Log($"分数 {currentScore} <= 阈值 {rule.scoreThreshold}。跳转到场景: {rule.sceneName}");
                SceneTransitionController.Instance.FadeToScene(rule.sceneName);
                return;
            }
        }
        
        Debug.Log($"分数 {currentScore} 高于所有阈值，停留在当前场景。");
    }
}