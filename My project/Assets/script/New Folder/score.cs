using UnityEngine;
using TMPro;

[RequireComponent(typeof(TextMeshProUGUI))]
public class ScoreTextUI : MonoBehaviour
{
    void Start()
    {
        TextMeshProUGUI scoreTextComponent = GetComponent<TextMeshProUGUI>();
        if (StoryManager.Instance != null)
        {
            StoryManager.Instance.RegisterScoreText(scoreTextComponent);
        }
        else
        {
            Debug.LogError("Could not find StoryManager instance to register ScoreText with!");
        }
    }
}