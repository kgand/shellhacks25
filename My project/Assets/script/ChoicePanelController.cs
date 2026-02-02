using UnityEngine;
using TMPro;
using UnityEngine.UI;
using System.Collections.Generic;

// 定义一个“选择”的数据结构
[System.Serializable]
public class Choice
{
    public string choiceText; // 按钮上显示的文字
    public int clarityChange; // 这个选择带来的分数变化
}

public class ChoicePanelController : MonoBehaviour
{
    public TextMeshProUGUI promptText;
    public List<Button> choiceButtons; // 把所有选项按钮拖到这里
    public List<TextMeshProUGUI> choiceButtonsText; // 把按钮下的Text拖到这里

    private List<Choice> currentChoices;

    void Start()
    {
        // 游戏开始时，默认隐藏自己
        gameObject.SetActive(false);
    }

    // 设置并显示选择面板
    public void SetupAndShow(string prompt, List<Choice> choices)
    {
        promptText.text = prompt;
        currentChoices = choices;

        for (int i = 0; i < choiceButtons.Count; i++)
        {
            if (i < choices.Count)
            {
                // 如果有这个选项，就激活按钮并设置内容
                choiceButtons[i].gameObject.SetActive(true);
                choiceButtonsText[i].text = choices[i].choiceText;
            }
            else
            {
                // 如果没有这个选项，就隐藏多余的按钮
                choiceButtons[i].gameObject.SetActive(false);
            }
        }
        
        gameObject.SetActive(true);
    }

    // 当一个按钮被点击时，这个方法会被调用
    public void MakeChoice(int buttonIndex)
    {
        if (buttonIndex < currentChoices.Count)
        {
            // 更新分数
            StoryManager.Instance.ChangeClarity(currentChoices[buttonIndex].clarityChange);
            // 隐藏面板
            gameObject.SetActive(false);
            // SceneTransitionController.Instance.FadeToScene("Scene_MemoryGarden"); 
        }
    }
}